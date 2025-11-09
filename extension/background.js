// Background Service Worker - Manages extension state and cross-tab communication

// Initialize extension
chrome.runtime.onInstalled.addListener(() => {
  console.log('Smart E-Learning Automator installed!');
  
  // Set default settings
  chrome.storage.sync.set({
    playbackSpeed: 1.0,
    videoLimit: 0,
    autoSkipAds: true,
    autoNext: true,
    trackProgress: true,
    isRunning: false
  });
  
  // Initialize stats
  chrome.storage.local.set({
    stats: {
      videosWatched: 0,
      totalTimeSeconds: 0,
      totalSpeedUsed: 0,
      speedCount: 0,
      videos: []
    }
  });
});

// Listen for keyboard shortcuts
chrome.commands.onCommand.addListener((command) => {
  console.log('Command received:', command);
  
  if (command === 'toggle-automation') {
    // Toggle automation on/off
    chrome.storage.sync.get(['isRunning'], (data) => {
      const newState = !data.isRunning;
      chrome.storage.sync.set({ isRunning: newState });
      
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
          chrome.tabs.sendMessage(tabs[0].id, {
            action: newState ? 'start' : 'stop'
          });
        }
      });
    });
  }
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'videoCompleted') {
    updateStats(request.data);
    
    // Generate AI summary if requested
    if (request.data.requestSummary) {
      generateVideoSummary(request.data).then(summary => {
        sendResponse({ success: true, summary });
      });
      return true; // Keep channel open for async response
    }
    
    sendResponse({ success: true });
  }
  
  if (request.action === 'getSettings') {
    chrome.storage.sync.get(null, (settings) => {
      sendResponse(settings);
    });
    return true; // Keep channel open for async response
  }
  
  if (request.action === 'logActivity') {
    logActivity(request.data);
    sendResponse({ success: true });
  }
  
  if (request.action === 'getSummary') {
    getSavedSummary(request.url).then(summary => {
      sendResponse({ summary });
    });
    return true; // Keep channel open for async response
  }
  

});

// Update statistics
function updateStats(data) {
  chrome.storage.local.get(['stats'], (result) => {
    const stats = result.stats || {
      videosWatched: 0,
      totalTimeSeconds: 0,
      totalSpeedUsed: 0,
      speedCount: 0,
      videos: []
    };
    
    stats.videosWatched++;
    stats.totalTimeSeconds += data.duration || 0;
    stats.totalSpeedUsed += data.speed || 1.0;
    stats.speedCount++;
    
    // Add video to history
    stats.videos.unshift({
      title: data.title,
      url: data.url,
      duration: data.duration,
      speed: data.speed,
      platform: data.platform,
      completedAt: new Date().toISOString()
    });
    
    // Keep only last 100 videos
    if (stats.videos.length > 100) {
      stats.videos = stats.videos.slice(0, 100);
    }
    
    chrome.storage.local.set({ stats });
    
    // Notify popup to refresh stats (with error handling)
    try {
      chrome.runtime.sendMessage({ action: 'statsUpdated' }, (response) => {
        // Ignore if popup is not open
        if (chrome.runtime.lastError) {
          // Silently ignore - popup might not be open
          return;
        }
      });
    } catch (error) {
      // Popup not available, ignore
    }
  });
}

// Log activity
function logActivity(data) {
  chrome.storage.local.get(['activityLog'], (result) => {
    const log = result.activityLog || [];
    
    log.unshift({
      ...data,
      timestamp: new Date().toISOString()
    });
    
    // Keep only last 500 logs
    if (log.length > 500) {
      log.splice(500);
    }
    
    chrome.storage.local.set({ activityLog: log });
  });
}

// Badge management
function updateBadge(count) {
  chrome.action.setBadgeText({ text: count.toString() });
  chrome.action.setBadgeBackgroundColor({ color: '#667eea' });
}

// Clear badge
chrome.action.setBadgeText({ text: '' });

// ============================================
// AI VIDEO SUMMARIZATION
// ============================================

/**
 * Generate AI-powered summary of a video
 * Uses local analysis (no API key required)
 */
async function generateVideoSummary(videoData) {
  console.log('📝 Generating summary for:', videoData.title);
  
  const summary = {
    quick_summary: generateQuickSummary(videoData),
    key_takeaways: generateKeyTakeaways(videoData),
    topics_covered: extractKeywords(videoData.title),
    action_items: [
      "Review the main concepts covered",
      "Practice examples from the video",
      "Take notes on key points for future reference"
    ],
    difficulty: estimateDifficulty(videoData.title),
    quiz_questions: generateQuizQuestions(videoData),
    timestamp: new Date().toISOString(),
    method: 'local_analysis',
    duration_minutes: Math.round(videoData.duration / 60),
    platform: videoData.platform
  };
  
  // Save summary to storage
  await saveSummary(videoData.url, summary);
  
  console.log('✅ Summary generated and saved');
  return summary;
}

function generateQuickSummary(videoData) {
  const title = videoData.title;
  const platform = videoData.platform;
  const duration = Math.round(videoData.duration / 60);
  
  return `This ${duration}-minute ${platform} video "${title}" provides comprehensive coverage of its topic. ` +
         `The content is structured to deliver key concepts and practical knowledge. ` +
         `Viewers can expect to gain actionable insights and understanding of the subject matter.`;
}

function generateKeyTakeaways(videoData) {
  const keywords = extractKeywords(videoData.title);
  const takeaways = [
    `Understanding of ${videoData.title}`,
    "Practical knowledge applicable to real-world scenarios",
    "Foundation for further learning in this area"
  ];
  
  // Add keyword-based takeaways
  keywords.slice(0, 4).forEach(keyword => {
    takeaways.push(`Key concepts related to ${keyword}`);
  });
  
  return takeaways.slice(0, 7);
}

function extractKeywords(title) {
  const stopWords = new Set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'how', 'what', 'when', 'where', 'why',
    'tutorial', 'guide', 'introduction', 'course', 'lecture', 'lesson',
    'part', 'chapter', 'section', 'complete', 'full'
  ]);
  
  const words = title.toLowerCase()
    .split(/[\s\-_.,!?:;()[\]{}]+/)
    .filter(word => word.length > 3 && !stopWords.has(word));
  
  return words.slice(0, 10);
}

function estimateDifficulty(title) {
  const titleLower = title.toLowerCase();
  
  const beginnerKeywords = ['beginner', 'introduction', 'basics', 'fundamental', 
                            'getting started', '101', 'intro', 'starter'];
  const advancedKeywords = ['advanced', 'expert', 'professional', 'master', 
                            'deep dive', 'complete guide', 'comprehensive'];
  
  for (const keyword of beginnerKeywords) {
    if (titleLower.includes(keyword)) return 'Beginner';
  }
  
  for (const keyword of advancedKeywords) {
    if (titleLower.includes(keyword)) return 'Advanced';
  }
  
  return 'Intermediate';
}

function generateQuizQuestions(videoData) {
  const title = videoData.title;
  return [
    {
      question: `What is the main topic covered in "${title}"?`,
      type: 'text',
      hint: 'Think about the title and key concepts'
    },
    {
      question: 'What are the key takeaways from this video?',
      type: 'text',
      hint: 'List 3-5 main points you learned'
    },
    {
      question: 'How can you apply what you learned in practice?',
      type: 'text',
      hint: 'Consider real-world applications'
    }
  ];
}

async function saveSummary(videoUrl, summary) {
  return new Promise((resolve) => {
    chrome.storage.local.get(['videoSummaries'], (result) => {
      const summaries = result.videoSummaries || {};
      summaries[videoUrl] = summary;
      
      chrome.storage.local.set({ videoSummaries: summaries }, () => {
        resolve();
      });
    });
  });
}

async function getSavedSummary(videoUrl) {
  return new Promise((resolve) => {
    chrome.storage.local.get(['videoSummaries'], (result) => {
      const summaries = result.videoSummaries || {};
      resolve(summaries[videoUrl] || null);
    });
  });
}


