"""
Unit tests for TalentScout Hiring Assistant.
Tests core functionality and data handling.
"""

import unittest
from unittest.mock import patch, MagicMock
from core import ConversationManager, PromptManager, ConversationState, CandidateInfo
from utils.data_handler import DataHandler
import tempfile
import shutil
import os
import json


class TestConversationManager(unittest.TestCase):
    """Test cases for ConversationManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = ConversationManager()
    
    def test_initialization(self):
        """Test manager initializes correctly."""
        self.assertEqual(self.manager.get_current_state(), ConversationState.GREETING)
        self.assertEqual(len(self.manager.conversation_history), 0)
        self.assertIsNotNone(self.manager.candidate_info)
    
    def test_exit_intent_detection(self):
        """Test exit keyword detection."""
        self.assertTrue(self.manager.is_exit_intent("exit"))
        self.assertTrue(self.manager.is_exit_intent("GOODBYE"))
        self.assertTrue(self.manager.is_exit_intent("I want to quit"))
        self.assertFalse(self.manager.is_exit_intent("next question"))
    
    def test_conversation_history(self):
        """Test conversation history tracking."""
        self.manager.add_to_history("user", "Hello")
        self.manager.add_to_history("assistant", "Hi there")
        
        self.assertEqual(len(self.manager.conversation_history), 2)
        self.assertEqual(self.manager.conversation_history[0]["role"], "user")
    
    def test_state_transitions(self):
        """Test state transitions."""
        self.manager.set_state(ConversationState.NAME_COLLECTION)
        self.assertEqual(self.manager.get_current_state(), ConversationState.NAME_COLLECTION)
    
    def test_candidate_info_update(self):
        """Test candidate information updates."""
        self.manager.update_candidate_info("full_name", "John Doe")
        self.assertEqual(self.manager.candidate_info.full_name, "John Doe")
    
    def test_technical_questions_management(self):
        """Test technical questions management."""
        questions = ["Q1", "Q2", "Q3"]
        self.manager.set_technical_questions(questions)
        
        self.assertTrue(self.manager.has_more_questions())
        q1 = self.manager.get_next_question()
        self.assertEqual(q1, "Q1")


class TestPromptManager(unittest.TestCase):
    """Test cases for PromptManager."""
    
    def test_system_prompt_generation(self):
        """Test system prompt is generated correctly."""
        prompt = PromptManager.get_system_prompt()
        self.assertIn("TalentScout", prompt)
        self.assertIn("hiring assistant", prompt)
    
    def test_greeting_prompt(self):
        """Test greeting prompt generation."""
        prompt = PromptManager.get_greeting_prompt()
        self.assertIsNotNone(prompt)
        self.assertGreater(len(prompt), 0)
    
    def test_info_gathering_prompts(self):
        """Test info gathering prompts."""
        fields = ["name", "email", "phone", "experience", "position", "location", "tech_stack"]
        for field in fields:
            prompt = PromptManager.get_info_gathering_prompt(field, "John")
            self.assertIsNotNone(prompt)
            self.assertGreater(len(prompt), 0)
    
    def test_tech_questions_generation_prompt(self):
        """Test technical questions generation prompt."""
        tech_stack = ["Python", "Django", "PostgreSQL"]
        prompt = PromptManager.get_tech_questions_generation_prompt(tech_stack)
        self.assertIn("Python", prompt)
        self.assertIn("Django", prompt)
        self.assertIn("PostgreSQL", prompt)


class TestCandidateInfo(unittest.TestCase):
    """Test cases for CandidateInfo."""
    
    def test_candidate_initialization(self):
        """Test candidate info initializes correctly."""
        candidate = CandidateInfo()
        self.assertIsNone(candidate.full_name)
        self.assertEqual(len(candidate.tech_stack), 0)
    
    def test_candidate_to_dict(self):
        """Test candidate conversion to dictionary."""
        candidate = CandidateInfo(
            full_name="John Doe",
            email="john@example.com",
            tech_stack=["Python", "Django"]
        )
        data = candidate.to_dict()
        self.assertEqual(data["full_name"], "John Doe")
        self.assertEqual(data["email"], "john@example.com")
        self.assertEqual(len(data["tech_stack"]), 2)


class TestDataHandler(unittest.TestCase):
    """Test cases for DataHandler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.handler = DataHandler(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_candidate_save_and_retrieve(self):
        """Test saving and retrieving candidate information."""
        candidate = CandidateInfo(
            full_name="Jane Doe",
            email="jane@example.com",
            phone="555-1234",
            years_of_experience="3",
            tech_stack=["JavaScript", "React"]
        )
        
        # Save candidate
        success = self.handler.save_candidate_info(candidate)
        self.assertTrue(success)
        
        # Retrieve all candidates
        candidates = self.handler.get_all_candidates()
        self.assertGreater(len(candidates), 0)
    
    def test_anonymization(self):
        """Test data anonymization."""
        candidate = CandidateInfo(
            full_name="John Doe",
            email="john@example.com"
        )
        
        anonymized = self.handler._anonymize_data(candidate)
        self.assertNotEqual(anonymized["full_name"], "John Doe")
        self.assertNotEqual(anonymized["email"], "john@example.com")
        self.assertEqual(len(anonymized["full_name"]), 16)  # Hash length
    
    def test_anonymous_id_generation(self):
        """Test anonymous ID generation."""
        id1 = self.handler._generate_anonymous_id("user1@example.com")
        id2 = self.handler._generate_anonymous_id("user2@example.com")
        
        self.assertNotEqual(id1, id2)
        self.assertTrue(id1.startswith("CAND_"))
        self.assertTrue(id2.startswith("CAND_"))
    
    def test_export_data(self):
        """Test data export functionality."""
        candidate = CandidateInfo(
            full_name="Test User",
            email="test@example.com",
            tech_stack=["Python"]
        )
        self.handler.save_candidate_info(candidate)
        
        # Export as JSON
        exported = self.handler.export_data(export_format="json")
        self.assertIsNotNone(exported)
        data = json.loads(exported)
        self.assertIsInstance(data, list)


class TestConversationFlow(unittest.TestCase):
    """Integration tests for conversation flow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = ConversationManager()
    
    def test_full_information_collection_flow(self):
        """Test complete information collection flow."""
        # Initial state
        self.assertEqual(self.manager.get_current_state(), ConversationState.GREETING)
        
        # Name collection
        self.manager.set_state(ConversationState.NAME_COLLECTION)
        self.manager.update_candidate_info("full_name", "Alice Smith")
        self.assertIsNotNone(self.manager.candidate_info.full_name)
        
        # Email collection
        self.manager.set_state(ConversationState.CONTACT_COLLECTION)
        self.manager.update_candidate_info("email", "alice@example.com")
        self.assertIsNotNone(self.manager.candidate_info.email)
        
        # Verify complete info check
        self.manager.update_candidate_info("phone", "555-1234")
        self.manager.update_candidate_info("years_of_experience", "5")
        self.manager.update_candidate_info("desired_positions", "Backend Developer")
        self.manager.update_candidate_info("current_location", "NYC")
        self.manager.update_candidate_info("tech_stack", ["Python", "Django"])
        
        self.assertTrue(self.manager.is_info_complete())


class TestDataPrivacy(unittest.TestCase):
    """Test cases for data privacy and GDPR compliance."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.handler = DataHandler(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_pii_hashing(self):
        """Test PII hashing for privacy."""
        pii = "john@example.com"
        hashed1 = self.handler._hash_pii(pii)
        hashed2 = self.handler._hash_pii(pii)
        
        # Same input should produce same hash
        self.assertEqual(hashed1, hashed2)
        
        # Different input should produce different hash
        hashed3 = self.handler._hash_pii("jane@example.com")
        self.assertNotEqual(hashed1, hashed3)
    
    def test_deletion_gdpr_right_to_be_forgotten(self):
        """Test GDPR right to be forgotten."""
        candidate = CandidateInfo(
            full_name="To Delete",
            email="delete@example.com"
        )
        
        self.handler.save_candidate_info(candidate)
        candidates = self.handler.get_all_candidates()
        initial_count = len(candidates)
        
        # Delete candidate
        anon_id = candidates[0]["anonymous_id"]
        success = self.handler.delete_candidate_info(anon_id)
        self.assertTrue(success)
        
        # Verify deletion
        candidates = self.handler.get_all_candidates()
        self.assertEqual(len(candidates), initial_count - 1)


if __name__ == "__main__":
    unittest.main()
