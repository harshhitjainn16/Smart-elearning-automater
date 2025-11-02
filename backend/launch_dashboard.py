"""
Launch Script for Enhanced Dashboard
Starts the new dashboard with authentication
"""
import subprocess
import sys
import os

print("=" * 70)
print(" SMART E-LEARNING AUTOMATOR - ENHANCED DASHBOARD")
print("=" * 70)
print()
print("🚀 Starting enhanced dashboard with login system...")
print()
print("Features:")
print("  ✅ User authentication & registration")
print("  ✅ Personalized progress tracking")
print("  ✅ Beautiful modern UI")
print("  ✅ User settings & preferences")
print("  ✅ Real-time automation monitoring")
print()
print("=" * 70)
print()

# Change to backend directory
os.chdir(os.path.dirname(__file__))

# Launch dashboard
subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'dashboard_v2.py'])
