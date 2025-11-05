```,```"""
Restart Dashboard Script
Kills existing Streamlit process and starts fresh
"""
import subprocess
import os
import sys
import time

print("🔄 Restarting Smart E-Learning Automator Dashboard...")
print("=" * 60)

# Kill existing Streamlit processes on Windows
print("\n1️⃣ Stopping existing dashboard...")
try:
    subprocess.run(
        ['taskkill', '/F', '/IM', 'streamlit.exe'],
        capture_output=True,
        text=True
    )
    print("   ✅ Stopped existing processes")
except:
    print("   ℹ️ No existing processes found")

# Also try to kill Python processes running Streamlit
try:
    result = subprocess.run(
        ['powershell', '-Command', 
         "Get-Process | Where-Object {$_.CommandLine -like '*streamlit*'} | Stop-Process -Force"],
        capture_output=True,
        text=True
    )
except:
    pass

time.sleep(2)

print("\n2️⃣ Starting fresh dashboard...")
print("   🌐 URL: http://localhost:8502")
print("   💡 Press Ctrl+C to stop")
print("=" * 60)

# Start new Streamlit instance with NEW dashboard (dashboard_v2.py with theme fix)
os.chdir(os.path.dirname(__file__))
subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'dashboard_v2.py'])

# After video completes:
# 1. Extract transcript
# 2. Use GPT-4/Claude to summarize
# 3. Create bullet points of key concepts
# 4. Highlight action items
# 5. Generate quiz questions

# Dashboard displays:
# - 3-sentence summary
# - Key takeaways
# - Recommended review sections
```
