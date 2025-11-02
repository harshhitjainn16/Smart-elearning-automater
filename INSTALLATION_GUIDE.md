# 🚀 Smart E-Learning Automator - Installation Guide

## For Individual Users (Browser Opens on Your Device)

Follow these steps to install and run the Smart E-Learning Automator on **your own computer**.

---

## ⚙️ Prerequisites

You'll need:
- **Windows 10/11** (or Mac/Linux)
- **Python 3.8 or newer**
- **Google Chrome** browser installed
- **15 minutes** for setup

---

## 📥 Step 1: Get Python

### Windows:
1. Go to: https://www.python.org/downloads/
2. Click **"Download Python 3.x.x"** (latest version)
3. Run the installer
4. ✅ **IMPORTANT:** Check the box "**Add Python to PATH**"
5. Click "Install Now"
6. Wait for installation to complete

### Verify Installation:
Open **Command Prompt** and type:
```cmd
python --version
```
You should see something like: `Python 3.11.x`

---

## 📂 Step 2: Get the Project Files

### Option A: Download from Friend
- Ask for the `smart-elearning-automater` folder
- Copy it to your computer (e.g., `C:\Users\YourName\Documents\`)

### Option B: Download from GitHub (if available)
```cmd
git clone https://github.com/yourusername/smart-elearning-automater.git
cd smart-elearning-automater
```

---

## 📦 Step 3: Install Required Packages

1. **Open Command Prompt** (Windows) or **Terminal** (Mac/Linux)

2. **Navigate to the backend folder:**
   ```cmd
   cd C:\Users\YourName\Documents\smart-elearning-automater\backend
   ```
   *(Replace with your actual path)*

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Wait for installation** (takes 2-5 minutes)

---

## ▶️ Step 4: Run the Dashboard

### Start the Application:
```cmd
streamlit run dashboard_v2.py
```

### What You'll See:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8502
Network URL: http://192.168.x.x:8502
```

**Your browser will automatically open!** 🎉

---

## 🎯 Step 5: Use the Application

1. **Register an Account**
   - Click the "📝 Register" tab
   - Fill in your details
   - Create your account

2. **Login**
   - Use your credentials to login

3. **Start Automation**
   - Paste a YouTube playlist URL
   - Set your preferred speed (0.5x - 2.0x)
   - Click "▶️ Start"
   - **Browser will open ON YOUR COMPUTER!** ✅

---

## 🔧 Troubleshooting

### Issue: "Python is not recognized"
**Solution:** You didn't add Python to PATH during installation.
- Reinstall Python
- Make sure to check "Add Python to PATH"

### Issue: "pip is not recognized"
**Solution:** Try using `python -m pip` instead:
```cmd
python -m pip install -r requirements.txt
```

### Issue: Chrome doesn't open
**Solution:** Make sure Google Chrome is installed:
- Download from: https://www.google.com/chrome/

### Issue: "Port 8502 is already in use"
**Solution:** Another instance is running.
- Close other Command Prompt windows
- Or use a different port:
  ```cmd
  streamlit run dashboard_v2.py --server.port 8503
  ```

### Issue: Module not found errors
**Solution:** Reinstall requirements:
```cmd
pip install --upgrade -r requirements.txt
```

---

## 🛑 How to Stop the Dashboard

Press **Ctrl + C** in the Command Prompt window where it's running.

---

## 🔄 Running It Again Later

You don't need to reinstall everything! Just:

1. **Open Command Prompt**
2. **Navigate to backend folder:**
   ```cmd
   cd C:\path\to\smart-elearning-automater\backend
   ```
3. **Run:**
   ```cmd
   streamlit run dashboard_v2.py
   ```

---

## 📱 Can I Access from My Phone?

Yes! While the dashboard is running:

1. **Find the Network URL** in the terminal output
2. **On your phone** (connected to same WiFi)
3. **Open browser** and go to that URL
4. **You can view** the dashboard, but:
   - ⚠️ Browser automation will still open on your **computer**, not phone
   - This is a limitation of how Selenium works

---

## 💡 Pro Tips

### Tip 1: Create a Shortcut
**Windows:**
Create a `.bat` file named `start_dashboard.bat`:
```batch
@echo off
cd C:\path\to\smart-elearning-automater\backend
streamlit run dashboard_v2.py
pause
```
Double-click to start!

### Tip 2: Auto-Start on Boot (Optional)
1. Press `Win + R`
2. Type `shell:startup`
3. Copy your `.bat` file here
4. Dashboard starts when you login!

### Tip 3: Bookmark the URL
Bookmark `http://localhost:8502` in your browser for quick access.

---

## 🎓 Features You'll Get

✅ **Auto-play videos** at customizable speeds (0.5x - 2.0x)
✅ **Skip ads** automatically
✅ **Track progress** with analytics dashboard
✅ **Quiz solving** (if enabled)
✅ **Multi-playlist** support
✅ **PDF reports** of your learning progress
✅ **Interactive charts** showing your activity
✅ **Theme switcher** (dark/light mode)

---

## 📞 Need Help?

If you encounter any issues:
1. Check the **Troubleshooting** section above
2. Make sure all prerequisites are installed
3. Contact the developer/admin

---

## ⚡ Quick Reference

| Command | Purpose |
|---------|---------|
| `python --version` | Check Python installation |
| `pip install -r requirements.txt` | Install dependencies |
| `streamlit run dashboard_v2.py` | Start dashboard |
| `Ctrl + C` | Stop dashboard |
| `http://localhost:8502` | Access dashboard |

---

**Happy Learning! 🎉**

