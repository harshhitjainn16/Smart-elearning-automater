/**
 * API Service for Smart E-Learning Automator Frontend
 * Handles communication with the FastAPI backend
 */

const API_BASE_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws';

class ApiService {
  constructor() {
    this.websocket = null;
    this.eventListeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000; // 3 seconds
  }

  /**
   * Make HTTP request to API
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    try {
      const response = await fetch(url, { ...defaultOptions, ...options });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: 'Unknown error' }));
        throw new Error(error.detail || error.message || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  /**
   * GET request
   */
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  /**
   * POST request
   */
  async post(endpoint, data = null) {
    const options = {
      method: 'POST',
    };
    
    if (data) {
      options.body = JSON.stringify(data);
    }
    
    return this.request(endpoint, options);
  }

  /**
   * Health check
   */
  async healthCheck() {
    return this.get('/health');
  }

  /**
   * Get automation status
   */
  async getStatus() {
    return this.get('/status');
  }

  /**
   * Start automation
   */
  async startAutomation(config) {
    return this.post('/automation/start', config);
  }

  /**
   * Stop automation
   */
  async stopAutomation() {
    return this.post('/automation/stop');
  }

  /**
   * Simulate quiz solving
   */
  async simulateQuiz() {
    return this.post('/quiz/simulate');
  }

  /**
   * Get statistics
   */
  async getStats() {
    return this.get('/stats');
  }

  /**
   * WebSocket connection management
   */
  connectWebSocket() {
    if (this.websocket?.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      this.websocket = new WebSocket(WS_URL);
      
      this.websocket.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.emit('connected', true);
      };

      this.websocket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.handleWebSocketMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.websocket.onclose = () => {
        console.log('WebSocket disconnected');
        this.emit('connected', false);
        this.attemptReconnect();
      };

      this.websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.emit('error', error);
      };

    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      this.attemptReconnect();
    }
  }

  /**
   * Handle incoming WebSocket messages
   */
  handleWebSocketMessage(message) {
    const { type, data } = message;
    
    switch (type) {
      case 'connection_established':
        this.emit('statusUpdate', data);
        break;
      case 'progress_update':
        this.emit('progressUpdate', data);
        break;
      case 'video_completed':
        this.emit('videoCompleted', data);
        break;
      case 'quiz_completed':
        this.emit('quizCompleted', data);
        break;
      case 'automation_started':
        this.emit('automationStarted', data);
        break;
      case 'automation_stopped':
        this.emit('automationStopped', data);
        break;
      case 'automation_completed':
        this.emit('automationCompleted', data);
        break;
      case 'automation_error':
        this.emit('automationError', data);
        break;
      case 'pong':
        // Handle ping/pong for connection health
        break;
      default:
        console.log('Unknown WebSocket message type:', type, data);
    }
  }

  /**
   * Attempt to reconnect WebSocket
   */
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting WebSocket reconnect ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
      
      setTimeout(() => {
        this.connectWebSocket();
      }, this.reconnectDelay);
    } else {
      console.error('Max WebSocket reconnect attempts reached');
      this.emit('reconnectFailed', true);
    }
  }

  /**
   * Send ping to keep connection alive
   */
  sendPing() {
    if (this.websocket?.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify({ type: 'ping' }));
    }
  }

  /**
   * Close WebSocket connection
   */
  disconnectWebSocket() {
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
  }

  /**
   * Event listener management
   */
  on(event, callback) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, new Set());
    }
    this.eventListeners.get(event).add(callback);
  }

  off(event, callback) {
    if (this.eventListeners.has(event)) {
      this.eventListeners.get(event).delete(callback);
    }
  }

  emit(event, data) {
    if (this.eventListeners.has(event)) {
      this.eventListeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in event listener for ${event}:`, error);
        }
      });
    }
  }

  /**
   * Cleanup
   */
  cleanup() {
    this.disconnectWebSocket();
    this.eventListeners.clear();
  }
}

// Create singleton instance
const apiService = new ApiService();

// Auto-connect WebSocket when service is imported
if (typeof window !== 'undefined') {
  apiService.connectWebSocket();
  
  // Send ping every 30 seconds to keep connection alive
  setInterval(() => {
    apiService.sendPing();
  }, 30000);
  
  // Cleanup on page unload
  window.addEventListener('beforeunload', () => {
    apiService.cleanup();
  });
}

export default apiService;