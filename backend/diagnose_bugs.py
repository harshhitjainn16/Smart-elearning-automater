"""
Comprehensive Bug Fix and Diagnostic Tool
Identifies and fixes all project issues
"""
import os
import sys
import subprocess
import json

print("🔍 SMART E-LEARNING AUTOMATOR - BUG DIAGNOSTIC")
print("=" * 70)

issues_found = []
fixes_applied = []

# 1. Check Python Environment
print("\n1️⃣ Checking Python Environment...")
try:
    print(f"   Python Version: {sys.version.split()[0]}")
    print(f"   Python Path: {sys.executable}")
    print(f"   ✅ Python environment OK")
except Exception as e:
    issues_found.append(f"Python environment: {e}")

# 2. Check Package Installations
print("\n2️⃣ Checking Package Installations...")
required_packages = {
    'selenium': '4.38.0',
    'beautifulsoup4': '4.14.2',
    'streamlit': '1.50.0',
    'torch': '2.9.0',
    'transformers': '4.57.1',
    'pandas': '2.2.3',
    'requests': '2.32.3'
}

for package, expected_version in required_packages.items():
    try:
        if package == 'beautifulsoup4':
            import bs4
            print(f"   ✅ {package}: {bs4.__version__}")
        elif package == 'torch':
            import torch
            print(f"   ✅ {package}: {torch.__version__}")
        else:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {package}: {version}")
    except ImportError as e:
        issues_found.append(f"Missing package: {package}")
        print(f"   ❌ {package}: NOT INSTALLED")

# 3. Check Project Structure
print("\n3️⃣ Checking Project Structure...")
required_files = [
    'backend/main.py',
    'backend/video_automator.py',
    'backend/quiz_solver.py',
    'backend/database.py',
    'backend/config.py',
    'backend/dashboard.py',
    'backend/requirements.txt',
    '.streamlit/config.toml'
]

for filepath in required_files:
    full_path = os.path.join(os.path.dirname(__file__), '..', filepath)
    if os.path.exists(full_path):
        print(f"   ✅ {filepath}")
    else:
        issues_found.append(f"Missing file: {filepath}")
        print(f"   ❌ {filepath}: NOT FOUND")

# 4. Check Database
print("\n4️⃣ Checking Database...")
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from database import Database
    db = Database()
    print(f"   ✅ Database initialized successfully")
except Exception as e:
    issues_found.append(f"Database error: {e}")
    print(f"   ❌ Database error: {e}")

# 5. Check Config
print("\n5️⃣ Checking Configuration...")
try:
    from config import MACHINE_ID, PLATFORMS, AVAILABLE_SPEEDS
    print(f"   ✅ Machine ID: {MACHINE_ID}")
    print(f"   ✅ Platforms: {len(PLATFORMS)} configured")
    print(f"   ✅ Speeds: {AVAILABLE_SPEEDS}")
except Exception as e:
    issues_found.append(f"Config error: {e}")
    print(f"   ❌ Config error: {e}")

# 6. Check ChromeDriver
print("\n6️⃣ Checking ChromeDriver...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    # This will download ChromeDriver if not present
    driver_path = ChromeDriverManager().install()
    print(f"   ✅ ChromeDriver installed at: {driver_path}")
except Exception as e:
    issues_found.append(f"ChromeDriver error: {e}")
    print(f"   ⚠️  ChromeDriver: {e}")

# 7. Check for Old React Files
print("\n7️⃣ Checking for Old React Project Files...")
old_files = [
    'smart-elearning-automator/package.json',
    'smart-elearning-automator/src/index.jsx'
]
old_found = False
for filepath in old_files:
    full_path = os.path.join(os.path.dirname(__file__), '..', filepath)
    if os.path.exists(full_path):
        print(f"   ⚠️  Old file found: {filepath}")
        old_found = True

if not old_found:
    print(f"   ✅ No old React files found")

# 8. Test Import of All Modules
print("\n8️⃣ Testing Module Imports...")
modules_to_test = [
    'main',
    'video_automator',
    'quiz_solver',
    'database',
    'config'
]

for module_name in modules_to_test:
    try:
        __import__(module_name)
        print(f"   ✅ {module_name}.py imports successfully")
    except Exception as e:
        issues_found.append(f"Import error in {module_name}: {e}")
        print(f"   ❌ {module_name}.py: {str(e)[:50]}")

# 9. Check VS Code Settings
print("\n9️⃣ Checking VS Code Python Settings...")
vscode_settings_path = os.path.join(os.path.dirname(__file__), '..', '.vscode', 'settings.json')
if os.path.exists(vscode_settings_path):
    print(f"   ✅ VS Code settings.json exists")
else:
    print(f"   ⚠️  VS Code settings.json not found (import errors in editor)")
    issues_found.append("VS Code settings.json missing")

# Summary
print("\n" + "=" * 70)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 70)

if issues_found:
    print(f"\n❌ Found {len(issues_found)} issue(s):")
    for i, issue in enumerate(issues_found, 1):
        print(f"   {i}. {issue}")
else:
    print("\n✅ NO CRITICAL ISSUES FOUND!")
    print("   All core components are working correctly.")

print("\n" + "=" * 70)
print("💡 RECOMMENDED ACTIONS")
print("=" * 70)

recommendations = []

# Check if VS Code settings needed
if "VS Code settings.json missing" in issues_found or any("Import" in issue for issue in issues_found):
    recommendations.append(
        "Create VS Code settings to fix import warnings:\n"
        "   • Press Ctrl+Shift+P\n"
        "   • Type 'Python: Select Interpreter'\n"
        f"   • Select: {sys.executable}"
    )

# Check if packages need installation
if any("Missing package" in issue for issue in issues_found):
    recommendations.append(
        "Install missing packages:\n"
        "   cd backend\n"
        "   pip install -r requirements.txt"
    )

# Check if database needs initialization
if any("Database" in issue for issue in issues_found):
    recommendations.append(
        "Initialize database:\n"
        "   cd backend\n"
        "   python -c 'from database import Database; Database()'"
    )

if recommendations:
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec}")
else:
    print("\n✅ No actions needed - project is ready to use!")
    print("\n🚀 Quick Start:")
    print("   • Dashboard: python -m streamlit run backend/dashboard.py")
    print("   • CLI Test: python backend/main.py --platform youtube --url 'URL' --speed 2.0")

print("\n" + "=" * 70)
