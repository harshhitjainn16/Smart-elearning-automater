// Popup JavaScript - Controls the extension UI

// DOM Elements
const speedSlider = document.getElementById('speedSlider');
const speedValue = document.getElementById('speedValue');
const videoLimit = document.getElementById('videoLimit');
const autoSkipAds = document.getElementById('autoSkipAds');
const autoNext = document.getElementById('autoNext');
const trackProgress = document.getElementById('trackProgress');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const statsBtn = document.getElementById('statsBtn');
const status = document.getElementById('status');
const progressSection = document.getElementById('progressSection');
const currentVideo = document.getElementById('currentVideo');
const progressFill = document.getElementById('progressFill');
const videoTime = document.getElementById('videoTime');

// Stats Elements
const videosWatched = document.getElementById('videosWatched');
const totalTime = document.getElementById('totalTime');
const avgSpeed = document.getElementById('avgSpeed');
const timeSaved = document.getElementById('timeSaved');

// Load saved settings
chrome.storage.sync.get([
  'playbackSpeed',
  'videoLimit',
  'autoSkipAds',
  'autoNext',
  'trackProgress',
  'isRunning'
], (data) => {
  speedSlider.value = data.playbackSpeed || 1;
  speedValue.textContent = data.playbackSpeed || 1;
  videoLimit.value = data.videoLimit || 0;
  autoSkipAds.checked = data.autoSkipAds !== false;
  autoNext.checked = data.autoNext !== false;
  trackProgress.checked = data.trackProgress !== false;
  
  if (data.isRunning) {
    updateUIRunning();
  }
});

// Load statistics
loadStatistics();

// Speed slider change
speedSlider.addEventListener('input', (e) => {
  const speed = parseFloat(e.target.value);
  speedValue.textContent = speed.toFixed(1);
  
  // Save to storage
  chrome.storage.sync.set({ playbackSpeed: speed });
  
  // Send to content script (with error handling)
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, {
        action: 'setSpeed',
        speed: speed
      }, (response) => {
        // Ignore errors if content script isn't loaded
        if (chrome.runtime.lastError) {
          // Silently ignore - this is expected on non-supported pages
          return;
        }
      });
    }
  });
});

// Save settings when changed
[videoLimit, autoSkipAds, autoNext, trackProgress].forEach(element => {
  element.addEventListener('change', saveSettings);
});

function saveSettings() {
  chrome.storage.sync.set({
    videoLimit: parseInt(videoLimit.value) || 0,
    autoSkipAds: autoSkipAds.checked,
    autoNext: autoNext.checked,
    trackProgress: trackProgress.checked
  });
}

// Start automation
startBtn.addEventListener('click', async () => {
  const settings = {
    playbackSpeed: parseFloat(speedSlider.value),
    videoLimit: parseInt(videoLimit.value) || 0,
    autoSkipAds: autoSkipAds.checked,
    autoNext: autoNext.checked,
    trackProgress: trackProgress.checked,
    isRunning: true
  };
  
  // Save settings
  await chrome.storage.sync.set(settings);
  
  // Check if we're on a supported platform
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    if (!tabs[0]) return;
    
    const url = tabs[0].url;
    const supportedPlatforms = [
      'youtube.com',
      'coursera.org',
      'udemy.com',
      'linkedin.com/learning',
      'skillshare.com'
    ];
    
    const isSupported = supportedPlatforms.some(platform => url && url.includes(platform));
    
    if (!isSupported) {
      alert('⚠️ Please navigate to a supported platform first!\n\n✅ Supported platforms:\n• YouTube (youtube.com)\n• Udemy (udemy.com)\n• Coursera (coursera.org)\n• LinkedIn Learning (linkedin.com/learning)\n• Skillshare (skillshare.com)');
      return;
    }
    
    // Determine which content script to inject
    let scriptFile = null;
    if (url.includes('youtube.com')) {
      scriptFile = 'content/youtube.js';
    } else if (url.includes('udemy.com')) {
      scriptFile = 'content/udemy.js';
    } else if (url.includes('coursera.org')) {
      scriptFile = 'content/coursera.js';
    } else if (url.includes('linkedin.com')) {
      scriptFile = 'content/linkedin.js';
    } else if (url.includes('skillshare.com')) {
      scriptFile = 'content/skillshare.js';
    }
    
    // Try to send message first
    chrome.tabs.sendMessage(tabs[0].id, {
      action: 'start',
      settings: settings
    }, async (response) => {
      if (chrome.runtime.lastError) {
        // Content script not loaded, inject it
        console.log('Content script not loaded, injecting:', scriptFile);
        
        if (scriptFile) {
          try {
            await chrome.scripting.executeScript({
              target: { tabId: tabs[0].id },
              files: [scriptFile]
            });
            
            // Wait a bit for script to load, then send message again
            setTimeout(() => {
              chrome.tabs.sendMessage(tabs[0].id, {
                action: 'start',
                settings: settings
              }, (response) => {
                if (response && response.success) {
                  updateUIRunning();
                } else {
                  alert('✅ Extension loaded! Please click "Start Automation" again.');
                }
              });
            }, 500);
          } catch (error) {
            console.error('Failed to inject script:', error);
            alert('❌ Failed to load automation script. Please reload the page and try again.');
          }
        }
      } else if (response && response.success) {
        updateUIRunning();
      } else if (response && response.success === false) {
        alert('⚠️ Could not start automation on this page.\n\nMake sure you\'re on a video/course page, not the homepage.');
      }
    });
  });
});

// Stop automation
stopBtn.addEventListener('click', () => {
  chrome.storage.sync.set({ isRunning: false });
  
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, {
        action: 'stop'
      }, (response) => {
        // Ignore errors if content script isn't loaded
        if (chrome.runtime.lastError) {
          return;
        }
      });
    }
  });
  
  updateUIIdle();
});

// View statistics
statsBtn.addEventListener('click', () => {
  chrome.tabs.create({ url: 'stats.html' });
});

// Update UI to running state
function updateUIRunning() {
  status.textContent = '▶️ Automation Active';
  status.classList.remove('idle');
  status.classList.add('active');
  startBtn.classList.add('hidden');
  stopBtn.classList.remove('hidden');
  progressSection.classList.remove('hidden');
}

// Update UI to idle state
function updateUIIdle() {
  status.textContent = '⏸️ Automation Idle';
  status.classList.remove('active');
  status.classList.add('idle');
  startBtn.classList.remove('hidden');
  stopBtn.classList.add('hidden');
  progressSection.classList.add('hidden');
}

// Load statistics from storage
function loadStatistics() {
  chrome.storage.local.get(['stats'], (data) => {
    const stats = data.stats || {
      videosWatched: 0,
      totalTimeSeconds: 0,
      totalSpeedUsed: 0,
      speedCount: 0
    };
    
    videosWatched.textContent = stats.videosWatched;
    totalTime.textContent = formatTime(stats.totalTimeSeconds);
    
    const avgSpeedVal = stats.speedCount > 0 ? stats.totalSpeedUsed / stats.speedCount : 1.0;
    avgSpeed.textContent = avgSpeedVal.toFixed(1) + 'x';
    
    const timeSavedSeconds = stats.totalTimeSeconds - (stats.totalTimeSeconds / avgSpeedVal);
    timeSaved.textContent = formatTime(timeSavedSeconds);
  });
}

// Format seconds to hours/minutes
function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }
  return `${minutes}m`;
}

// Listen for updates from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'updateProgress') {
    currentVideo.textContent = request.title || 'Playing...';
    progressFill.style.width = request.progress + '%';
    videoTime.textContent = `${request.currentTime} / ${request.duration}`;
  }
  
  if (request.action === 'statsUpdated') {
    loadStatistics();
  }
  
  if (request.action === 'summaryGenerated') {
    // Show notification that summary is ready
    console.log('✅ Summary generated for video');
    loadSummaries();
  }
});

// Refresh stats every 5 seconds when popup is open
setInterval(loadStatistics, 5000);

// ============================================
// AI SUMMARIES FEATURE
// ============================================

const summaryBtn = document.getElementById('summaryBtn');
const summariesSection = document.getElementById('summariesSection');
const summariesList = document.getElementById('summariesList');

summaryBtn.addEventListener('click', () => {
  const isHidden = summariesSection.classList.contains('hidden');
  summariesSection.classList.toggle('hidden');
  
  if (isHidden) {
    summaryBtn.textContent = '✖️ Hide Summaries';
    loadSummaries();
  } else {
    summaryBtn.textContent = '📝 View Summaries';
  }
});

async function loadSummaries() {
  chrome.storage.local.get(['videoSummaries'], (result) => {
    const summaries = result.videoSummaries || {};
    const summaryEntries = Object.entries(summaries);
    
    if (summaryEntries.length === 0) {
      summariesList.innerHTML = '<p style="text-align: center; opacity: 0.7;">No summaries yet. Complete a video to generate summary!</p>';
      return;
    }
    
    // Sort by timestamp (newest first)
    summaryEntries.sort((a, b) => {
      const timeA = a[1].timestamp || '';
      const timeB = b[1].timestamp || '';
      return timeB.localeCompare(timeA);
    });
    
    // Show only last 5 summaries
    const recentSummaries = summaryEntries.slice(0, 5);
    
    summariesList.innerHTML = recentSummaries.map(([url, summary]) => {
      const date = summary.timestamp ? new Date(summary.timestamp).toLocaleDateString() : 'Unknown date';
      const takeaways = summary.key_takeaways || [];
      
      return `
        <div class="summary-item">
          <h4>📹 ${summary.platform || 'Video'}</h4>
          <div class="summary-text">${summary.quick_summary || 'Summary unavailable'}</div>
          
          ${takeaways.length > 0 ? `
            <details>
              <summary style="cursor: pointer; opacity: 0.8; font-size: 12px;">View Takeaways (${takeaways.length})</summary>
              <ul class="takeaways">
                ${takeaways.slice(0, 5).map(takeaway => `<li>${takeaway}</li>`).join('')}
              </ul>
            </details>
          ` : ''}
          
          <div class="summary-meta">
            <span>${date} • ${summary.duration_minutes || 0} min</span>
            <span class="summary-badge">${summary.difficulty || 'Intermediate'}</span>
          </div>
        </div>
      `;
    }).join('');
  });
}


