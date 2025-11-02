import React, { useState, useEffect, useCallback } from 'react';
import { Play, Pause, SkipForward, Brain, CheckCircle, Activity, Settings, Book, Award, Clock, TrendingUp, Zap, Database, Globe } from 'lucide-react';

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

  useEffect(() => {
    if (isAutomating) {
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            setCurrentVideo(v => v + 1);
            setVideoStatus('completed');
            const currentVid = currentVideo;
            addLog(`Video ${currentVid} completed successfully`, 'success');
            setTimeout(() => {
              setVideoStatus('playing');
              addLog(`Starting video ${currentVid + 1}`, 'info');
            }, 1000);
            return 0;
          }
          return prev + 2;
        });
      }, 100);
      return () => clearInterval(interval);
    }
  }, [isAutomating, currentVideo, addLog]);

  const handleAutomate = () => {
    if (!isAutomating) {
      setIsAutomating(true);
      setVideoStatus('playing');
      addLog('Automation started - Initializing AI models', 'success');
      setTimeout(() => addLog('Connected to learning platform', 'info'), 500);
    } else {
      setIsAutomating(false);
      setVideoStatus('paused');
      addLog('Automation paused by user', 'warning');
    }
  };

  const handleQuizSimulation = () => {
    setTotalQuizzes(prev => prev + 1);
    const correct = Math.random() > 0.1;
    if (correct) setQuizScore(prev => prev + 1);
    addLog(`Quiz ${totalQuizzes + 1}: ${correct ? 'Correct answer submitted' : 'Needs review'}`, correct ? 'success' : 'warning');
    setAiAccuracy((quizScore + (correct ? 1 : 0)) / (totalQuizzes + 1) * 100);
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
            <select className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none">
              <option>Coursera</option>
              <option>Udemy</option>
              <option>YouTube Playlists</option>
              <option>Moodle</option>
              <option>Custom Platform</option>
            </select>
          </div>
          <div>
            <label className="text-slate-400 text-sm mb-2 block">Playlist URL</label>
            <input type="text" placeholder="https://example.com/playlist/123" className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 border border-slate-600 focus:border-cyan-500 focus:outline-none" />
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
              <div className="text-white font-semibold">Save Quiz Answers</div>
              <div className="text-slate-400 text-sm">Store answers for future reference</div>
            </div>
            <div className="w-12 h-6 bg-cyan-500 rounded-full flex items-center px-1">
              <div className="w-4 h-4 bg-white rounded-full ml-auto"></div>
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
          <div className="flex items-center gap-4 mb-2">
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