import React, { useState, useEffect, useCallback } from 'react';
import { Play, Pause, SkipForward, Brain, CheckCircle, Activity, Settings, Book, Award, Clock, TrendingUp, Zap, Database, Globe, Wifi, WifiOff } from 'lucide-react';
import apiService from '../services/apiService';

const SmartELearningAutomator = () => {
  const [isAutomating, setIsAutomating] = useState(false);
  const [currentVideo, setCurrentVideo] = useState(1);
  const [progress, setProgress] = useState(0);
  const [quizScore, setQuizScore] = useState(0);
  const [totalQuizzes, setTotalQuizzes] = useState(0);
  const [logs, setLogs] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [videoStatus, setVideoStatus] = useState('idle');
  const [aiAccuracy, setAiAccuracy] = useState(94.5);
  const [isConnected, setIsConnected] = useState(false);
  const [backendError, setBackendError] = useState(null);
  const [config, setConfig] = useState({
    platform: 'youtube',
    playlist_url: '',
    username: '',
    password: '',
    auto_quiz: true,
    video_limit: 5,
    playback_speed: 1.0
  });

  const stats = [
    { icon: Book, label: 'Videos Completed', value: currentVideo - 1, color: 'from-purple-500 to-pink-500' },
    { icon: Award, label: 'Quiz Accuracy', value: `${aiAccuracy}%`, color: 'from-cyan-500 to-blue-500' },
    { icon: Clock, label: 'Time Saved', value: '12.5h', color: 'from-orange-500 to-red-500' },
    { icon: TrendingUp, label: 'Success Rate', value: '98%', color: 'from-green-500 to-emerald-500' }
  ];

  const addLog = useCallback((message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [{timestamp, message, type}, ...prev.slice(0, 9)]);
  }, []);

  // Initialize API service and WebSocket
  useEffect(() => {
    // Set up event listeners
    apiService.on('connected', setIsConnected);
    apiService.on('error', (error) => {
      setBackendError(error.message || 'Connection error');
      addLog('Backend connection error', 'error');
    });
    apiService.on('reconnectFailed', () => {
      setBackendError('Unable to connect to backend');
      addLog('Failed to connect to backend after multiple attempts', 'error');
    });

    // Real-time updates
    apiService.on('statusUpdate', (data) => {
      setIsAutomating(data.is_running);
      setCurrentVideo(data.current_video);
      setProgress(data.progress);
      setVideoStatus(data.video_status);
      if (data.stats) {
        setAiAccuracy(data.stats.quiz_accuracy || 94.5);
      }
    });

    apiService.on('progressUpdate', (data) => {
      setProgress(data.progress);
      setCurrentVideo(data.current_video);
      setVideoStatus(data.video_status);
    });

    apiService.on('videoCompleted', (data) => {
      addLog(`Video ${data.video_number} completed successfully`, 'success');
      setVideoStatus('completed');
    });

    apiService.on('quizCompleted', (data) => {
      const message = `Quiz completed: ${data.correct ? 'Correct' : 'Needs review'} (${data.confidence.toFixed(1)}% confidence)`;
      addLog(message, data.correct ? 'success' : 'warning');
      setAiAccuracy(data.new_accuracy);
      setTotalQuizzes(prev => prev + 1);
      if (data.correct) setQuizScore(prev => prev + 1);
    });

    apiService.on('automationStarted', (data) => {
      setIsAutomating(true);
      setVideoStatus('playing');
      addLog(`Automation started for ${data.platform}`, 'success');
    });

    apiService.on('automationStopped', () => {
      setIsAutomating(false);
      setVideoStatus('stopped');
      addLog('Automation stopped by user', 'warning');
    });

    apiService.on('automationCompleted', (data) => {
      setIsAutomating(false);
      setVideoStatus('completed');
      addLog(`Automation completed! ${data.total_videos} videos processed`, 'success');
    });

    apiService.on('automationError', (data) => {
      setIsAutomating(false);
      setVideoStatus('error');
      addLog(`Automation error: ${data.error}`, 'error');
    });

    // Check initial connection
    apiService.healthCheck()
      .then(() => {
        setBackendError(null);
        addLog('Connected to backend successfully', 'success');
      })
      .catch((error) => {
        setBackendError(error.message);
        addLog('Backend not available', 'error');
      });

    // Cleanup on unmount
    return () => {
      apiService.cleanup();
    };
  }, [addLog]);

  // Real automation control (replaces simulation)
  const handleAutomate = async () => {
    if (!isAutomating) {
      try {
        if (!config.playlist_url) {
          addLog('Please enter a playlist URL first', 'warning');
          return;
        }

        addLog('Starting automation...', 'info');
        await apiService.startAutomation(config);
      } catch (error) {
        addLog(`Failed to start automation: ${error.message}`, 'error');
        setBackendError(error.message);
      }
    } else {
      try {
        addLog('Stopping automation...', 'info');
        await apiService.stopAutomation();
      } catch (error) {
        addLog(`Failed to stop automation: ${error.message}`, 'error');
      }
    }
  };



  const handleQuizSimulation = async () => {
    try {
      addLog('Testing quiz AI...', 'info');
      await apiService.simulateQuiz();
    } catch (error) {
      addLog(`Quiz simulation failed: ${error.message}`, 'error');
    }
  };

  const DashboardView = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, idx) => (
          <div key={idx} className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700 hover:border-slate-600 transition-all hover:scale-105">
            <div className={`bg-gradient-to-r ${stat.color} w-12 h-12 rounded-xl flex items-center justify-center mb-4`}>
              <stat.icon className="w-6 h-6 text-white" />
            </div>
            <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
            <div className="text-slate-400 text-sm">{stat.label}</div>
          </div>
        ))}
      </div>

      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 border border-slate-700">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-2xl font-bold text-white mb-2">Current Progress</h3>
            <p className="text-slate-400">Video {currentVideo} - {videoStatus === 'playing' ? 'Playing' : videoStatus === 'completed' ? 'Completed' : 'Ready'}</p>
          </div>
          <div className={`px-4 py-2 rounded-full ${isAutomating ? 'bg-green-500/20 text-green-400' : 'bg-slate-700 text-slate-400'} font-semibold flex items-center gap-2`}>
            <Activity className={`w-4 h-4 ${isAutomating ? 'animate-pulse' : ''}`} />
            {isAutomating ? 'Active' : 'Idle'}
          </div>
        </div>
        
        <div className="mb-4">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-slate-400">Video Progress</span>
            <span className="text-cyan-400 font-semibold">{progress}%</span>
          </div>
          <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300 rounded-full"
              style={{width: `${progress}%`}}
            />
          </div>
        </div>

        <div className="flex gap-4 mt-6">
          <button 
            onClick={handleAutomate}
            className={`flex-1 ${isAutomating ? 'bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600' : 'bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600'} text-white font-semibold py-4 px-6 rounded-xl transition-all flex items-center justify-center gap-2 hover:scale-105`}
          >
            {isAutomating ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
            {isAutomating ? 'Pause Automation' : 'Start Automation'}
          </button>
          <button 
            onClick={handleQuizSimulation}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold py-4 px-6 rounded-xl transition-all flex items-center gap-2 hover:scale-105"
          >
            <Brain className="w-5 h-5" />
            Test Quiz AI
          </button>
        </div>
      </div>

      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-yellow-400" />
          Activity Logs
        </h3>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {logs.length === 0 ? (
            <p className="text-slate-500 text-center py-8">No activity yet. Start automation to see logs.</p>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className={`p-3 rounded-lg border ${
                log.type === 'success' ? 'bg-green-500/10 border-green-500/30 text-green-400' :
                log.type === 'warning' ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400' :
                'bg-blue-500/10 border-blue-500/30 text-blue-400'
              }`}>
                <span className="text-xs opacity-75">{log.timestamp}</span>
                <span className="ml-3">{log.message}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );

  const SettingsView = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Globe className="w-5 h-5 text-cyan-400" />
          Platform Configuration
        </h3>
        <div className="space-y-4">
          <div>
            <label className="text-slate-400 text-sm mb-2 block">Learning Platform</label>
            <select 
              value={config.platform}
              onChange={(e) => setConfig(prev => ({ ...prev, platform: e.target.value }))}
              className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none"
            >
              <option value="coursera">Coursera</option>
              <option value="udemy">Udemy</option>
              <option value="youtube">YouTube Playlists</option>
              <option value="moodle">Moodle</option>
            </select>
          </div>
          <div>
            <label className="text-slate-400 text-sm mb-2 block">Playlist URL</label>
            <input 
              type="text" 
              placeholder="https://example.com/playlist/123" 
              value={config.playlist_url}
              onChange={(e) => setConfig(prev => ({ ...prev, playlist_url: e.target.value }))}
              className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none" 
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-slate-400 text-sm mb-2 block">Username (optional)</label>
              <input 
                type="text" 
                placeholder="your@email.com" 
                value={config.username}
                onChange={(e) => setConfig(prev => ({ ...prev, username: e.target.value }))}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none" 
              />
            </div>
            <div>
              <label className="text-slate-400 text-sm mb-2 block">Password (optional)</label>
              <input 
                type="password" 
                placeholder="••••••••" 
                value={config.password}
                onChange={(e) => setConfig(prev => ({ ...prev, password: e.target.value }))}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none" 
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-slate-400 text-sm mb-2 block">Video Limit</label>
              <input 
                type="number" 
                min="1"
                max="50"
                value={config.video_limit}
                onChange={(e) => setConfig(prev => ({ ...prev, video_limit: parseInt(e.target.value) }))}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none" 
              />
            </div>
            <div>
              <label className="text-slate-400 text-sm mb-2 block">Playback Speed</label>
              <select 
                value={config.playback_speed}
                onChange={(e) => setConfig(prev => ({ ...prev, playback_speed: parseFloat(e.target.value) }))}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none"
              >
                <option value={0.5}>0.5x</option>
                <option value={0.75}>0.75x</option>
                <option value={1.0}>1.0x (Normal)</option>
                <option value={1.25}>1.25x</option>
                <option value={1.5}>1.5x</option>
                <option value={1.75}>1.75x</option>
                <option value={2.0}>2.0x</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Brain className="w-5 h-5 text-purple-400" />
          AI Configuration
        </h3>
        <div className="space-y-4">
          <div>
            <label className="text-slate-400 text-sm mb-2 block">AI Model</label>
            <select className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none">
              <option>GPT-4 (Recommended)</option>
              <option>BERT</option>
              <option>Custom Trained Model</option>
            </select>
          </div>
          <div>
            <label className="text-slate-400 text-sm mb-2 block">Confidence Threshold: 85%</label>
            <input type="range" min="50" max="100" defaultValue="85" className="w-full" />
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Database className="w-5 h-5 text-green-400" />
          Data Storage
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-slate-700 rounded-lg">
            <div>
              <div className="text-white font-semibold">Auto-solve Quizzes</div>
              <div className="text-slate-400 text-sm">Automatically solve quizzes using AI</div>
            </div>
            <div 
              className={`w-12 h-6 ${config.auto_quiz ? 'bg-cyan-500' : 'bg-slate-600'} rounded-full flex items-center px-1 cursor-pointer`}
              onClick={() => setConfig(prev => ({ ...prev, auto_quiz: !prev.auto_quiz }))}
            >
              <div className={`w-4 h-4 bg-white rounded-full transition-all ${config.auto_quiz ? 'ml-auto' : ''}`}></div>
            </div>
          </div>
          <div className="flex items-center justify-between p-4 bg-slate-700 rounded-lg">
            <div>
              <div className="text-white font-semibold">Track Progress</div>
              <div className="text-slate-400 text-sm">Log video completion history</div>
            </div>
            <div className="w-12 h-6 bg-cyan-500 rounded-full flex items-center px-1">
              <div className="w-4 h-4 bg-white rounded-full ml-auto"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-4">
              <div className="bg-gradient-to-r from-cyan-500 to-blue-500 p-3 rounded-2xl">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">
                  SMART E-LEARNING AUTOMATOR
                </h1>
                <p className="text-slate-400 mt-1">AI-Powered Learning Automation Platform</p>
              </div>
            </div>
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${
              isConnected ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
            }`}>
              {isConnected ? <Wifi className="w-4 h-4" /> : <WifiOff className="w-4 h-4" />}
              <span className="font-semibold">
                {isConnected ? 'Connected' : backendError || 'Disconnected'}
              </span>
            </div>
          </div>
        </div>

        <div className="flex gap-4 mb-6">
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${
              activeTab === 'dashboard' 
                ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            <Activity className="w-5 h-5" />
            Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('settings')}
            className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${
              activeTab === 'settings' 
                ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            <Settings className="w-5 h-5" />
            Settings
          </button>
        </div>

        {activeTab === 'dashboard' ? <DashboardView /> : <SettingsView />}

        <div className="mt-8 text-center text-slate-500 text-sm">
          <p>⚡ Powered by AI • Selenium • NLP Models • Smart Automation</p>
        </div>
      </div>
    </div>
  );
};

export default SmartELearningAutomator;