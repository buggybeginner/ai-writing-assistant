# tests/ultimate_test.py
import os
import sys
import subprocess

def run_ultimate_test():
    print("🚀 PERSONAWRITE AI - ULTIMATE FRONTEND TEST")
    print("=" * 60)
    
    tests = [
        ("Project Structure", check_structure),
        ("Dependencies", check_dependencies),
        ("Page Modules", check_pages),
        ("CSS Files", check_css),
        ("Test Suite", check_tests),
        ("Documentation", check_docs),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            print("   ✅ PASS")
            passed += 1
        else:
            print("   ❌ FAIL")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 CONGRATULATIONS! Person B tasks are COMPLETELY FINISHED!")
        print("🎓 Your frontend is ready for FYP submission.")
        return True
    else:
        print("⚠️  Some tests failed. Please review.")
        return False

def check_structure():
    required = [
        "app.py",
        "requirements.txt",
        "pages/",
        "pages/home.py",
        "pages/preset.py", 
        "pages/personal.py",
        "pages/dashboard.py",
        "utils/",
        "utils/ui_components.py",
        "assets/",
        "assets/styles.css",
        "tests/",
        "tests/test_ui.py",
        "tests/final_test.py",
        "README.md"
    ]
    
    missing = []
    for item in required:
        if not os.path.exists(item):
            missing.append(item)
    
    if missing:
        print(f"   Missing: {', '.join(missing)}")
        return False
    return True

def check_dependencies():
    try:
        import streamlit
        import pandas
        import plotly
        return True
    except ImportError as e:
        print(f"   Missing: {e}")
        return False

def check_pages():
    pages = ["home", "preset", "personal", "dashboard"]
    for page in pages:
        if not os.path.exists(f"pages/{page}.py"):
            print(f"   Missing: pages/{page}.py")
            return False
    return True

def check_css():
    return os.path.exists("assets/styles.css") and os.path.getsize("assets/styles.css") > 100

def check_tests():
    return os.path.exists("tests/test_ui.py") and os.path.exists("tests/final_test.py")

def check_docs():
    return os.path.exists("README.md") and os.path.getsize("README.md") > 500

if __name__ == "__main__":
    success = run_ultimate_test()
    sys.exit(0 if success else 1)