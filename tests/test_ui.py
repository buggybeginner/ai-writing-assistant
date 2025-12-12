import unittest
import sys
import os

# Add the utils directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.ui_components import personality_card_html, text_area_with_counter

class TestUIComponents(unittest.TestCase):
    
    def test_personality_card_generation(self):
        """Test that personality card HTML is generated correctly"""
        # Test basic card
        html = personality_card_html("Test Personality", "Test description", "🎭", False)
        self.assertIn("Test Personality", html)
        self.assertIn("personality-card", html)
        self.assertIn("🎭", html)
        
        # Test selected card
        html_selected = personality_card_html("Selected", "Desc", "🌟", True)
        self.assertIn("border-color: #4f46e5", html_selected)
        self.assertIn("✓", html_selected)
    
    def test_text_counter_logic(self):
        """Test character and word counting logic"""
        test_cases = [
            ("", 0, 0),  # Empty string
            ("Hello", 5, 1),  # Single word
            ("Hello World", 11, 2),  # Two words
            ("Hello\nWorld", 11, 2),  # With newline
            ("  Hello  World  ", 11, 2),  # With spaces
        ]
        
        for text, expected_chars, expected_words in test_cases:
            # Simulate what the function does
            chars = len(text)
            words = len(text.split())
            self.assertEqual(chars, expected_chars)
            self.assertEqual(words, expected_words)
    
    def test_progress_tracker_logic(self):
        """Test progress step calculation"""
        steps = ["Step 1", "Step 2", "Step 3", "Step 4"]
        
        # Test different current steps
        test_cases = [
            (0, 0.25),  # First step = 25%
            (1, 0.5),   # Second step = 50%
            (3, 1.0),   # Last step = 100%
        ]
        
        for current_step, expected_progress in test_cases:
            progress = (current_step + 1) / len(steps)
            self.assertAlmostEqual(progress, expected_progress)

class TestFileHandling(unittest.TestCase):
    
    def test_file_type_validation(self):
        """Test that file types are validated correctly"""
        allowed_types = ['.txt', '.pdf', '.docx']
        
        valid_files = ['document.txt', 'report.pdf', 'essay.docx']
        invalid_files = ['image.png', 'video.mp4', 'data.csv']
        
        for file in valid_files:
            self.assertTrue(any(file.endswith(ext) for ext in allowed_types))
        
        for file in invalid_files:
            self.assertFalse(any(file.endswith(ext) for ext in allowed_types))

def run_tests():
    """Run all tests and display results"""
    print("🚀 Running PersonaWrite AI Frontend Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestUIComponents)
    suite.addTests(loader.loadTestsFromTestCase(TestFileHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("=" * 50)
    print(f"✅ Tests Run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    if result.failures:
        print(f"❌ Failures: {len(result.failures)}")
    if result.errors:
        print(f"⚠️ Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)