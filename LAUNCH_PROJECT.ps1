# Smart E-Learning Automator - Complete Launcher
# Launches BOTH Extension + Dashboard

Write-Host "`n=========================================================" -ForegroundColor Cyan
Write-Host "   SMART E-LEARNING AUTOMATOR - FULL SUITE" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "`n"

Write-Host "This will launch:" -ForegroundColor Yellow
Write-Host "  1. Chrome Extension (Browser Automation)" -ForegroundColor White
Write-Host "  2. Streamlit Dashboard (Analytics)" -ForegroundColor White
Write-Host "`n"

# ============================================
# PART 1: LAUNCH CHROME EXTENSION
# ============================================

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "PART 1: CHROME EXTENSION SETUP" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "`n"

$extensionPath = "D:\Harshit\Harshit C++\smart-elearning-automater\extension"

Write-Host "Extension Location:" -ForegroundColor Yellow
Write-Host "   $extensionPath" -ForegroundColor White
Write-Host "`n"

Write-Host "Opening Chrome Extensions Page..." -ForegroundColor Yellow
Start-Process "chrome://extensions/"
Start-Sleep -Seconds 2

Write-Host "Opening Extension Folder in Explorer..." -ForegroundColor Yellow
explorer $extensionPath
Start-Sleep -Seconds 1

Write-Host "`nChrome Extension Setup Steps:" -ForegroundColor Green
Write-Host "   1. In Chrome, enable 'Developer mode' (top-right toggle)" -ForegroundColor White
Write-Host "   2. Click 'Load unpacked' button" -ForegroundColor White
Write-Host "   3. Select the opened folder: extension" -ForegroundColor White
Write-Host "   4. Extension will appear with purple icon" -ForegroundColor White
Write-Host "`n"

Write-Host "Press any key to continue to Dashboard setup..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# ============================================
# PART 2: LAUNCH STREAMLIT DASHBOARD
# ============================================

Write-Host "`n"
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "PART 2: STREAMLIT DASHBOARD LAUNCH" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "`n"

$backendPath = "D:\Harshit\Harshit C++\smart-elearning-automater\backend"

Write-Host "Stopping any existing dashboard processes..." -ForegroundColor Yellow
try {
    Stop-Process -Name "streamlit" -Force -ErrorAction SilentlyContinue
    Write-Host "   Stopped existing processes" -ForegroundColor Green
} catch {
    Write-Host "   No existing processes found" -ForegroundColor Gray
}

Start-Sleep -Seconds 2

Write-Host "`nStarting Streamlit Dashboard..." -ForegroundColor Yellow
Write-Host "`n"
Write-Host "=========================================================" -ForegroundColor Magenta
Write-Host "          DASHBOARD WILL OPEN AT:" -ForegroundColor Yellow
Write-Host "          http://localhost:8501" -ForegroundColor Cyan
Write-Host "          (Browser will auto-open in ~5 seconds)" -ForegroundColor White
Write-Host "=========================================================" -ForegroundColor Magenta
Write-Host "`n"

Write-Host "Dashboard Features:" -ForegroundColor Yellow
Write-Host "   - Real-time automation control" -ForegroundColor White
Write-Host "   - Video statistics and analytics" -ForegroundColor White
Write-Host "   - Platform configuration" -ForegroundColor White
Write-Host "   - Progress tracking" -ForegroundColor White
Write-Host "   - Light/Dark theme toggle" -ForegroundColor White
Write-Host "`n"

Write-Host "To STOP the dashboard: Press Ctrl+C in this window" -ForegroundColor Red
Write-Host "`n"
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "`n"

# Change to backend directory and run NEW dashboard (with theme fix)
Set-Location $backendPath
python -m streamlit run dashboard_v2.py

Write-Host "`n"
Write-Host "Dashboard stopped." -ForegroundColor Red
Write-Host "`n"
