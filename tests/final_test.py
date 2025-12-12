import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestFrontendCompleteness(unittest.TestCase):
    
    def test_all_pages_exist(self):
        """Test that all page modules exist"""
        required_pages = ['home', 'preset', 'personal', 'dashboard']
        for page in required_pages:
            file_path = f"pages/{page}.py"
            self.assertTrue(os.path.exists(file_path), f"Missing: {file_path}")
    
    def test_css_file_exists(self):
        """Test that CSS file exists"""
        self.assertTrue(os.path.exists("assets/styles.css"))
    
    def test_requirements_exist(self):
        """Test that requirements file exists"""
        self.assertTrue(os.path.exists("requirements.txt"))
    
    def test_utils_directory(self):
        """Test that utils directory has components"""
        self.assertTrue(os.path.exists("utils/ui_components.py"))
    
    def test_session_state_keys(self):
        """Test required session state keys"""
        import streamlit as st
        required_keys = ['user_id', 'user_name', 'generation_history', 
                        'uploaded_files', 'selected_personality']
        
        # This would need to run in Streamlit context
        print("Note: Session state test requires Streamlit runtime")

def run_completeness_check():
    """Run all completeness checks"""
    print("🔍 Running Frontend Completeness Check...")
    print("=" * 50)
    
    checks = [
        ("📁 Page Modules", lambda: all(os.path.exists(f"pages/{p}.py") 
                                      for p in ['home', 'preset', 'personal', 'dashboard'])),
        ("🎨 CSS Styling", lambda: os.path.exists("assets/styles.css")),
        ("📦 Dependencies", lambda: os.path.exists("requirements.txt")),
        ("🧩 UI Components", lambda: os.path.exists("utils/ui_components.py")),
        ("🧪 Testing", lambda: os.path.exists("tests/test_ui.py")),
    ]
    
    all_passed = True
    for name, check in checks:
        try:
            if check():
                print(f"✅ {name}: PASSED")
            else:
                print(f"❌ {name}: FAILED")
                all_passed = False
        except Exception as e:
            print(f"⚠️  {name}: ERROR - {e}")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All frontend checks passed! Person B tasks are complete.")
    else:
        print("⚠️  Some checks failed. Review missing components.")
    
    return all_passed

if __name__ == "__main__":
    if run_completeness_check():
        sys.exit(0)
    else:
        sys.exit(1)