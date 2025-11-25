"""
Data handler for TalentScout Hiring Assistant.
Manages secure storage, anonymization, and GDPR compliance for candidate information.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import hashlib
import secrets
from core import CandidateInfo


class DataHandler:
    """
    Handles secure storage and management of candidate information.
    Implements GDPR compliance and data privacy best practices.
    """

    def __init__(self, data_dir: str = "data/candidate_info"):
        """
        Initialize the data handler.
        
        Args:
            data_dir: Directory for storing candidate information
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Encryption salt (in production, use environment variable)
        self.salt = os.getenv("DATA_SALT", "salt_2024_talentscout").encode()

    def save_candidate_info(self, candidate: CandidateInfo) -> bool:
        """
        Save candidate information to storage.
        
        Args:
            candidate: CandidateInfo object to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate anonymized ID
            anon_id = self._generate_anonymous_id(candidate.email or candidate.full_name)
            
            # Create candidate data with metadata
            candidate_data = {
                "anonymous_id": anon_id,
                "timestamp": datetime.now().isoformat(),
                "data": self._anonymize_data(candidate),
                "version": "1.0"
            }
            
            # Save to file
            filename = self.data_dir / f"{anon_id}.json"
            with open(filename, 'w') as f:
                json.dump(candidate_data, f, indent=2)
            
            # Create log entry
            self._log_activity("CANDIDATE_SAVED", anon_id, "Candidate information saved securely")
            
            return True
        except Exception as e:
            print(f"Error saving candidate information: {e}")
            self._log_activity("SAVE_ERROR", "", str(e))
            return False

    def retrieve_candidate_info(self, anonymous_id: str) -> Optional[Dict]:
        """
        Retrieve candidate information by anonymous ID.
        
        Args:
            anonymous_id: The anonymous ID of the candidate
            
        Returns:
            Dictionary with candidate info or None if not found
        """
        try:
            filename = self.data_dir / f"{anonymous_id}.json"
            if not filename.exists():
                return None
            
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self._log_activity("CANDIDATE_RETRIEVED", anonymous_id, "Candidate information retrieved")
            return data
        except Exception as e:
            print(f"Error retrieving candidate information: {e}")
            return None

    def delete_candidate_info(self, anonymous_id: str) -> bool:
        """
        Delete candidate information (GDPR right to be forgotten).
        
        Args:
            anonymous_id: The anonymous ID of the candidate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filename = self.data_dir / f"{anonymous_id}.json"
            if filename.exists():
                filename.unlink()
                self._log_activity("CANDIDATE_DELETED", anonymous_id, "Candidate information deleted per GDPR request")
                return True
            return False
        except Exception as e:
            print(f"Error deleting candidate information: {e}")
            self._log_activity("DELETE_ERROR", anonymous_id, str(e))
            return False

    def get_all_candidates(self) -> list:
        """
        Get list of all stored candidates (anonymized).
        
        Returns:
            List of candidate summaries
        """
        try:
            candidates = []
            for file in self.data_dir.glob("*.json"):
                with open(file, 'r') as f:
                    data = json.load(f)
                candidates.append({
                    "anonymous_id": data.get("anonymous_id"),
                    "timestamp": data.get("timestamp"),
                    "tech_stack": data.get("data", {}).get("tech_stack", [])
                })
            return candidates
        except Exception as e:
            print(f"Error retrieving candidates: {e}")
            return []

    def export_data(self, export_format: str = "json") -> str:
        """
        Export all data in specified format (GDPR data portability).
        
        Args:
            export_format: Format for export ("json" or "csv")
            
        Returns:
            Exported data as string
        """
        try:
            candidates = []
            for file in self.data_dir.glob("*.json"):
                with open(file, 'r') as f:
                    candidates.append(json.load(f))
            
            if export_format == "json":
                return json.dumps(candidates, indent=2)
            elif export_format == "csv":
                return self._convert_to_csv(candidates)
            else:
                return json.dumps(candidates, indent=2)
        except Exception as e:
            print(f"Error exporting data: {e}")
            return ""

    def _anonymize_data(self, candidate: CandidateInfo) -> Dict:
        """
        Anonymize sensitive candidate information.
        
        Args:
            candidate: CandidateInfo object
            
        Returns:
            Dictionary with anonymized data
        """
        return {
            "full_name": self._hash_pii(candidate.full_name) if candidate.full_name else None,
            "email": self._hash_pii(candidate.email) if candidate.email else None,
            "phone": self._hash_pii(candidate.phone) if candidate.phone else None,
            "years_of_experience": candidate.years_of_experience,
            "desired_positions": candidate.desired_positions,
            "current_location": candidate.current_location,
            "tech_stack": candidate.tech_stack,
            "technical_responses_count": len(candidate.technical_responses)
        }

    def _hash_pii(self, data: str) -> str:
        """
        Hash personally identifiable information for anonymization.
        
        Args:
            data: Data to hash
            
        Returns:
            Hashed data
        """
        return hashlib.sha256(data.encode() + self.salt).hexdigest()[:16]

    def _generate_anonymous_id(self, identifier: str) -> str:
        """
        Generate an anonymous ID from an identifier.
        
        Args:
            identifier: Identifier (email, name, etc.)
            
        Returns:
            Anonymous ID
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = secrets.token_hex(4)
        return f"CAND_{timestamp}_{random_suffix}"

    def _log_activity(self, activity: str, candidate_id: str, details: str):
        """
        Log data access and modification activities for audit trail.
        
        Args:
            activity: Type of activity
            candidate_id: Candidate ID (can be anonymous)
            details: Activity details
        """
        try:
            log_file = self.data_dir / ".." / "activity_log.json"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "activity": activity,
                "candidate_id": candidate_id,
                "details": details
            }
            
            # Append to log file
            logs = []
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"Error logging activity: {e}")

    def _convert_to_csv(self, candidates: list) -> str:
        """
        Convert candidate data to CSV format.
        
        Args:
            candidates: List of candidate dictionaries
            
        Returns:
            CSV formatted string
        """
        if not candidates:
            return ""
        
        # Extract headers from first candidate's data
        headers = list(candidates[0].get("data", {}).keys())
        headers = ["anonymous_id", "timestamp"] + headers
        
        # Build CSV
        csv_lines = [",".join(headers)]
        for candidate in candidates:
            row = [
                candidate.get("anonymous_id", ""),
                candidate.get("timestamp", ""),
            ]
            for header in headers[2:]:
                value = candidate.get("data", {}).get(header, "")
                if isinstance(value, list):
                    value = ";".join(value)
                row.append(str(value))
            csv_lines.append(",".join(row))
        
        return "\n".join(csv_lines)

    def cleanup_old_data(self, days: int = 90) -> int:
        """
        Delete data older than specified number of days (GDPR retention policy).
        
        Args:
            days: Number of days to retain
            
        Returns:
            Number of files deleted
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            deleted_count = 0
            
            for file in self.data_dir.glob("*.json"):
                with open(file, 'r') as f:
                    data = json.load(f)
                
                file_timestamp = datetime.fromisoformat(data.get("timestamp", ""))
                if file_timestamp < cutoff_date:
                    file.unlink()
                    deleted_count += 1
                    self._log_activity("OLD_DATA_DELETED", data.get("anonymous_id"), 
                                      f"Deleted data older than {days} days")
            
            return deleted_count
        except Exception as e:
            print(f"Error cleaning up old data: {e}")
            return 0


# Example usage
if __name__ == "__main__":
    from core import CandidateInfo
    
    # Create sample candidate
    sample_candidate = CandidateInfo(
        full_name="John Doe",
        email="john@example.com",
        phone="555-1234",
        years_of_experience="5",
        desired_positions="Backend Developer",
        current_location="New York",
        tech_stack=["Python", "Django", "PostgreSQL"]
    )
    
    # Test data handler
    handler = DataHandler()
    print("Saving candidate...")
    success = handler.save_candidate_info(sample_candidate)
    print(f"Save successful: {success}")
    
    print("\nRetrieving all candidates...")
    candidates = handler.get_all_candidates()
    print(f"Found {len(candidates)} candidates")
