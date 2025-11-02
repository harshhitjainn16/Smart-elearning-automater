"""
Test Installation Script
Verifies all components are working
"""
import sys
print("Testing Smart E-Learning Automator installation...\n")

# Test 1: Core imports
print("1. Testing core imports...")
try:
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import requests
    print("   ✓ Selenium, BeautifulSoup, Requests")
except ImportError as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 2: ML/NLP imports
print("2. Testing ML/NLP packages...")
try:
    import torch
    from transformers import pipeline
    print(f"   ✓ PyTorch {torch.__version__}")
    print(f"   ✓ Transformers")
except ImportError as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 3: Project modules
print("3. Testing project modules...")
try:
    from database import Database
    from config import PLATFORMS
    print("   ✓ Database module")
    print("   ✓ Config module")
except ImportError as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 4: Database initialization
print("4. Testing database...")
try:
    db = Database()
    db.add_log('test', 'Installation test', 'success')
    logs = db.get_recent_logs(limit=1)
    assert len(logs) > 0
    print("   ✓ Database working")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 5: Platform configs
print("5. Testing platform configurations...")
try:
    assert 'youtube' in PLATFORMS
    assert 'coursera' in PLATFORMS
    assert 'udemy' in PLATFORMS
    assert 'moodle' in PLATFORMS
    print(f"   ✓ {len(PLATFORMS)} platforms configured")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✅ ALL TESTS PASSED!")
print("="*50)
print("\nYour Smart E-Learning Automator is ready!")
print("\nNext steps:")
print("  • Test with YouTube: python main.py --platform youtube --url 'YOUR_URL' --limit 1")
print("  • Launch dashboard: streamlit run dashboard.py")
print("  • Read docs: See README.md and QUICKSTART.md")
