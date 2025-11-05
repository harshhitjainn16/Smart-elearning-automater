"""
Start the Smart E-Learning Automator API Server
"""
import uvicorn
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting Smart E-Learning Automator Backend...")
    print("📡 API Server: http://localhost:8000")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("📊 API Docs: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )