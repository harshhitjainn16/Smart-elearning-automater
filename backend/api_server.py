"""
FastAPI server for Smart E-Learning Automator
Provides REST API endpoints for frontend communication
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from video_automator import VideoAutomator
from database import Database
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Smart E-Learning Automator API",
    description="Backend API for AI-powered learning automation",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
automation_state = {
    "is_running": False,
    "current_video": 1,
    "progress": 0,
    "video_status": "idle",
    "platform": "",
    "playlist_url": "",
    "automator": None,
    "stats": {
        "videos_completed": 0,
        "quiz_accuracy": 94.5,
        "time_saved": "0h",
        "success_rate": 98
    }
}

# WebSocket connections
connected_clients = set()

# Request/Response Models
class AutomationConfig(BaseModel):
    platform: str
    playlist_url: str
    username: Optional[str] = None
    password: Optional[str] = None
    auto_quiz: bool = True
    video_limit: Optional[int] = None
    playback_speed: float = 1.0

class AutomationResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: dict):
        if self.active_connections:
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error broadcasting: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for conn in disconnected:
                self.disconnect(conn)

manager = ConnectionManager()

# Automation thread function
def automation_thread(config: AutomationConfig):
    """Run automation in separate thread"""
    global automation_state
    
    try:
        logger.info(f"Starting automation thread for {config.platform}")
        
        # Initialize automator
        automator = VideoAutomator(
            platform=config.platform, 
            headless=True,  # Run in headless mode for API
            playback_speed=config.playback_speed
        )
        
        automation_state["automator"] = automator
        automator.init_driver()
        
        # Login if credentials provided
        if config.username and config.password:
            credentials = {"username": config.username, "password": config.password}
            automator.login(credentials)
        
        # Navigate to playlist
        automator.navigate_to_playlist(config.playlist_url)
        
        # Simulate automation progress
        video_count = 0
        max_videos = config.video_limit or 5  # Default to 5 for demo
        
        while automation_state["is_running"] and video_count < max_videos:
            # Simulate video progress
            for progress in range(0, 101, 5):
                if not automation_state["is_running"]:
                    break
                    
                automation_state["progress"] = progress
                automation_state["video_status"] = "playing"
                
                # Broadcast progress update
                asyncio.run(manager.broadcast({
                    "type": "progress_update",
                    "data": {
                        "progress": progress,
                        "current_video": automation_state["current_video"],
                        "video_status": automation_state["video_status"]
                    }
                }))
                
                time.sleep(0.5)  # Simulate video time
            
            if automation_state["is_running"]:
                # Video completed
                video_count += 1
                automation_state["current_video"] = video_count + 1
                automation_state["progress"] = 0
                automation_state["video_status"] = "completed"
                automation_state["stats"]["videos_completed"] = video_count
                
                # Broadcast completion
                asyncio.run(manager.broadcast({
                    "type": "video_completed",
                    "data": {
                        "video_number": video_count,
                        "total_completed": video_count
                    }
                }))
                
                # Brief pause between videos
                time.sleep(2)
        
        # Automation completed
        automation_state["is_running"] = False
        automation_state["video_status"] = "completed"
        
        asyncio.run(manager.broadcast({
            "type": "automation_completed",
            "data": {"total_videos": video_count}
        }))
        
    except Exception as e:
        logger.error(f"Automation thread error: {e}")
        automation_state["is_running"] = False
        automation_state["video_status"] = "error"
        
        asyncio.run(manager.broadcast({
            "type": "automation_error",
            "data": {"error": str(e)}
        }))
    
    finally:
        if automation_state["automator"]:
            automation_state["automator"].close()
            automation_state["automator"] = None

# API Endpoints

@app.get("/")
async def root():
    return {"message": "Smart E-Learning Automator API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/status")
async def get_automation_status():
    """Get current automation status"""
    return AutomationResponse(
        success=True,
        message="Status retrieved successfully",
        data={
            "is_running": automation_state["is_running"],
            "current_video": automation_state["current_video"],
            "progress": automation_state["progress"],
            "video_status": automation_state["video_status"],
            "platform": automation_state["platform"],
            "stats": automation_state["stats"]
        }
    )

@app.post("/automation/start")
async def start_automation(config: AutomationConfig):
    """Start automation with given configuration"""
    
    if automation_state["is_running"]:
        raise HTTPException(status_code=400, detail="Automation already running")
    
    try:
        # Update state
        automation_state.update({
            "is_running": True,
            "platform": config.platform,
            "playlist_url": config.playlist_url,
            "current_video": 1,
            "progress": 0,
            "video_status": "initializing"
        })
        
        # Start automation in background thread
        thread = threading.Thread(
            target=automation_thread, 
            args=(config,), 
            daemon=True
        )
        thread.start()
        
        # Broadcast start event
        await manager.broadcast({
            "type": "automation_started",
            "data": {
                "platform": config.platform,
                "playlist_url": config.playlist_url
            }
        })
        
        return AutomationResponse(
            success=True,
            message="Automation started successfully",
            data={"platform": config.platform}
        )
        
    except Exception as e:
        logger.error(f"Error starting automation: {e}")
        automation_state["is_running"] = False
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation/stop")
async def stop_automation():
    """Stop current automation"""
    
    if not automation_state["is_running"]:
        raise HTTPException(status_code=400, detail="No automation running")
    
    try:
        automation_state["is_running"] = False
        automation_state["video_status"] = "stopped"
        
        # Close automator if exists
        if automation_state["automator"]:
            automation_state["automator"].close()
            automation_state["automator"] = None
        
        # Broadcast stop event
        await manager.broadcast({
            "type": "automation_stopped",
            "data": {"stopped_at": datetime.now().isoformat()}
        })
        
        return AutomationResponse(
            success=True,
            message="Automation stopped successfully"
        )
        
    except Exception as e:
        logger.error(f"Error stopping automation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quiz/simulate")
async def simulate_quiz():
    """Simulate AI quiz solving"""
    try:
        # Simulate AI processing
        import random
        is_correct = random.random() > 0.1  # 90% success rate
        confidence = random.uniform(80, 98)
        
        # Update stats
        current_accuracy = automation_state["stats"]["quiz_accuracy"]
        automation_state["stats"]["quiz_accuracy"] = (current_accuracy + confidence) / 2
        
        # Broadcast quiz result
        await manager.broadcast({
            "type": "quiz_completed",
            "data": {
                "correct": is_correct,
                "confidence": confidence,
                "new_accuracy": automation_state["stats"]["quiz_accuracy"]
            }
        })
        
        return AutomationResponse(
            success=True,
            message="Quiz simulation completed",
            data={
                "correct": is_correct,
                "confidence": confidence,
                "accuracy": automation_state["stats"]["quiz_accuracy"]
            }
        )
        
    except Exception as e:
        logger.error(f"Error in quiz simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get automation statistics"""
    try:
        db = Database()
        
        # Get real stats from database if available
        stats = automation_state["stats"].copy()
        
        try:
            # Try to get real quiz stats
            quiz_stats = db.get_quiz_stats("all")
            if quiz_stats:
                stats.update(quiz_stats)
        except:
            pass  # Use default stats if database not available
        
        return AutomationResponse(
            success=True,
            message="Statistics retrieved successfully",
            data=stats
        )
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    
    try:
        # Send initial status
        await manager.send_personal_message({
            "type": "connection_established",
            "data": {
                "is_running": automation_state["is_running"],
                "current_video": automation_state["current_video"],
                "progress": automation_state["progress"],
                "stats": automation_state["stats"]
            }
        }, websocket)
        
        # Keep connection alive
        while True:
            # Wait for messages from client (ping/pong)
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )