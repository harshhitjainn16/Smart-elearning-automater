// Skillshare Content Script

let isAutomationRunning = false;
let settings = {};
let videosWatchedCount = 0;
let currentVideoData = {};
let videoEndHandlerAttached = false;
let userPausedVideo = false;  // Track if user manually paused
let lastPlayTime = 0;          // Track when video was last playing

console.log('🎓 Smart E-Learning Automator loaded on Skillshare');
console.log('Current URL:', window.location.href);

// Safe message sending with error handling
function safeSendMessage(message, callback) {
  try {
    chrome.runtime.sendMessage(message, (response) => {
      if (chrome.runtime.lastError) {
        console.log('Extension reloaded, message not sent');
        return;
      }
      if (callback) callback(response);
    });
  } catch (error) {
    console.log('Could not send message:', error.message);
  }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Skillshare content script received message:', request.action);
  
  if (request.action === 'start') {
    settings = request.settings;
    console.log('Starting Skillshare automation with settings:', settings);
    startAutomation();
    sendResponse({ success: true });
  }
  
  if (request.action === 'stop') {
    stopAutomation();
    sendResponse({ success: true });
  }
  
  if (request.action === 'setSpeed') {
    setPlaybackSpeed(request.speed);
    sendResponse({ success: true });
  }
  
  if (request.action === 'getCurrentTimestamp') {
    const video = document.querySelector('video');
    if (video) {
      const timestamp = Math.floor(video.currentTime);
      const videoTitle = document.querySelector('h1')?.textContent?.trim() ||
                        document.title.split('|')[0]?.trim() ||
                        'Skillshare Video';
      
      sendResponse({ 
        success: true, 
        timestamp: timestamp,
        formattedTime: formatTime(timestamp),
        videoTitle: videoTitle,
        videoUrl: window.location.href,
        platform: 'skillshare'
      });
    } else {
      sendResponse({ success: false, error: 'No video found' });
    }
  }
  
  if (request.action === 'jumpToTimestamp') {
    const video = document.querySelector('video');
    if (video && request.timestamp !== undefined) {
      video.currentTime = request.timestamp;
      sendResponse({ success: true });
    } else {
      sendResponse({ success: false, error: 'Cannot jump to timestamp' });
    }
  }
  
  return true;
});

chrome.storage.sync.get(['isRunning'], (data) => {
  if (data.isRunning) {
    chrome.storage.sync.get(null, (allSettings) => {
      settings = allSettings;
      startAutomation();
    });
  }
});

function startAutomation() {
  isAutomationRunning = true;
  console.log('▶️ Skillshare automation started');
  
  safeSendMessage({
    action: 'logActivity',
    data: {
      type: 'automation_start',
      message: 'Automation started on Skillshare',
      url: window.location.href
    }
  });
  
  setPlaybackSpeed(settings.playbackSpeed);
  monitorVideo();
  
  if (settings.autoNext) {
    setupAutoNext();
  }
}

function stopAutomation() {
  isAutomationRunning = false;
  console.log('⏹️ Skillshare automation stopped');
}

function setPlaybackSpeed(speed) {
  const video = document.querySelector('video');
  if (video) {
    video.playbackRate = speed;
    console.log(`⚡ Speed set to ${speed}x`);
  }
}

function monitorVideo() {
  const video = document.querySelector('video');
  if (!video) {
    setTimeout(monitorVideo, 1000);
    return;
  }
  
  const titleElement = document.querySelector('.session-item.selected h3') || 
                       document.querySelector('.class-details-header h1');
  const title = titleElement ? titleElement.textContent.trim() : 'Unknown Lesson';
  
  currentVideoData = {
    title: title,
    url: window.location.href,
    platform: 'skillshare',
    speed: settings.playbackSpeed || 1.0,
    startTime: Date.now()
  };
  
  const progressInterval = setInterval(() => {
    if (!isAutomationRunning) {
      clearInterval(progressInterval);
      return;
    }
    
    if (video.duration) {
      const progress = (video.currentTime / video.duration) * 100;
      safeSendMessage({
        action: 'updateProgress',
        title: title,
        progress: Math.round(progress),
        currentTime: formatTime(video.currentTime),
        duration: formatTime(video.duration)
      });
    }
  }, 1000);
  
  if (videoEndHandlerAttached) {
    video.removeEventListener('ended', handleVideoEnd);
  }
  
  video.addEventListener('ended', handleVideoEnd, { once: true });
  videoEndHandlerAttached = true;
  
  // Track user pause/play actions
  video.addEventListener('pause', () => {
    if (!video.ended && video.currentTime > 0 && video.currentTime < video.duration - 1) {
      userPausedVideo = true;
      console.log('⏸️ User paused video - automation will not auto-resume');
    }
  });
  
  video.addEventListener('play', () => {
    userPausedVideo = false;
    lastPlayTime = Date.now();
  });
  
  video.addEventListener('playing', () => {
    lastPlayTime = Date.now();
  });
  
  video.addEventListener('loadedmetadata', () => {
    setPlaybackSpeed(settings.playbackSpeed);
  });
}

function handleVideoEnd() {
  if (!isAutomationRunning) return;
  
  const video = document.querySelector('video');
  currentVideoData.duration = video ? video.duration : 0;
  
  videosWatchedCount++;
  
  safeSendMessage({
    action: 'videoCompleted',
    data: currentVideoData
  });
  
  console.log(`✅ Lesson ${videosWatchedCount} completed: ${currentVideoData.title}`);
  
  videoEndHandlerAttached = false;
  
  if (settings.videoLimit > 0 && videosWatchedCount >= settings.videoLimit) {
    console.log('🛑 Lesson limit reached');
    stopAutomation();
    alert('Lesson limit reached! Automation stopped.');
    return;
  }
  
  // Let Skillshare's autoplay handle progression
  if (settings.autoNext) {
    console.log('⏭️ Waiting for Skillshare autoplay to load next lesson...');
  }
}

// Play next lesson (only called manually, not after video end)
function playNextLesson() {
  // Check if there's a project or quiz
  const isProject = window.location.href.includes('/projects') || 
                    document.querySelector('.project-container');
  
  if (isProject) {
    console.log('📝 Project/Assignment detected - attempting to skip');
    skipProject();
    return;
  }
  
  const nextSelectors = [
    'button.next-session-btn',
    '.session-item.selected + .session-item',
    'button[aria-label="Next lesson"]'
  ];
  
  for (const selector of nextSelectors) {
    const nextButton = document.querySelector(selector);
    if (nextButton) {
      nextButton.click();
      console.log('⏭️ Moving to next lesson');
      setTimeout(monitorVideo, 2000);
      return;
    }
  }
  
  console.log('📝 No next lesson found');
  stopAutomation();
}

// Skip project/assignment pages
function skipProject() {
  console.log('🔍 Attempting to skip project/assignment...');
  
  const skipSelectors = [
    'button:contains("Skip")',
    'a:contains("Next Lesson")',
    'button.next-session-btn',
    '.session-item.selected + .session-item'
  ];
  
  for (const selector of skipSelectors) {
    const skipButton = document.querySelector(selector);
    if (skipButton) {
      console.log(`✅ Found skip/next button: ${selector}`);
      skipButton.click();
      setTimeout(monitorVideo, 2000);
      return;
    }
  }
  
  // Try to navigate via session list
  const currentSession = document.querySelector('.session-item.selected');
  if (currentSession) {
    const nextSession = currentSession.nextElementSibling;
    if (nextSession) {
      console.log('📚 Moving to next session via session list');
      nextSession.click();
      setTimeout(monitorVideo, 2000);
      return;
    }
  }
  
  console.log('⚠️ Could not find way to skip project');
  stopAutomation();
}

function setupAutoNext() {
  console.log('✅ Auto-next enabled for Skillshare');
  
  // Auto-resume paused videos (but respect user pause)
  setInterval(() => {
    if (!isAutomationRunning) return;
    
    const video = document.querySelector('video');
    if (!video) return;
    
    // Don't auto-resume if user manually paused
    if (userPausedVideo) {
      return;
    }
    
    // Only auto-play if video is paused and not ended
    if (video.paused && !video.ended && video.currentTime > 0) {
      const timeSinceLastPlay = Date.now() - lastPlayTime;
      if (timeSinceLastPlay > 3000) {
        const playButton = document.querySelector('button[aria-label="Play"]') ||
                          document.querySelector('.vjs-play-control') ||
                          document.querySelector('.play-button');
        if (playButton) {
          playButton.click();
          console.log('▶️ Auto-clicked play button (after 3s pause)');
        }
      }
    }
  }, 4000);
}

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  
  if (h > 0) {
    return `${h}:${pad(m)}:${pad(s)}`;
  }
  return `${m}:${pad(s)}`;
}

function pad(num) {
  return num.toString().padStart(2, '0');
}

let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    console.log('🔄 URL changed:', url);
    
    if (!isAutomationRunning) return;
    
    // Reset user pause flag on new page
    userPausedVideo = false;
    
    if (url.includes('/classes/')) {
      // Check if it's a project page
      if (url.includes('/projects')) {
        console.log('📝 Project page detected - attempting to skip');
        setTimeout(() => {
          skipProject();
        }, 1500);
      } else {
        console.log('📺 New lesson detected');
        setTimeout(monitorVideo, 1500);
      }
    }
  }
}).observe(document, { subtree: true, childList: true });
