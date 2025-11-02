"""
Test Video Playback Speed Feature
Demonstrates how to use different playback speeds
"""
print("=" * 70)
print("🎬 VIDEO PLAYBACK SPEED FEATURE")
print("=" * 70)

print("\n📊 Available Speeds:")
speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
for speed in speeds:
    time_saved = (1.0 - (1.0 / speed)) * 100 if speed > 1.0 else 0
    description = "Normal" if speed == 1.0 else f"Save {time_saved:.0f}% time" if speed > 1.0 else "Slower"
    print(f"  • {speed}x - {description}")

print("\n" + "=" * 70)
print("💡 USAGE EXAMPLES")
print("=" * 70)

print("\n1️⃣  Command Line (CLI):")
print("   " + "-" * 60)
print("   # Normal speed (1x)")
print("   python main.py --platform youtube --url 'URL' --speed 1.0")
print()
print("   # 2x speed (watch faster, save 50% time)")
print("   python main.py --platform youtube --url 'URL' --speed 2.0")
print()
print("   # 1.5x speed (balanced - save 33% time)")
print("   python main.py --platform coursera --url 'URL' --speed 1.5")

print("\n2️⃣  Dashboard (GUI):")
print("   " + "-" * 60)
print("   python -m streamlit run dashboard.py")
print("   Then select speed from dropdown: ⚡ Playback Speed")

print("\n3️⃣  Programmatic Usage:")
print("   " + "-" * 60)
print("   from video_automator import VideoAutomator")
print()
print("   # Initialize with speed")
print("   automator = VideoAutomator('youtube', playback_speed=2.0)")
print()
print("   # Or change speed later")
print("   automator.set_playback_speed(1.5)")

print("\n" + "=" * 70)
print("⏱️  TIME SAVINGS CALCULATOR")
print("=" * 70)

video_duration = 60  # 60 minutes
print(f"\nFor a {video_duration}-minute video:\n")

for speed in [1.0, 1.25, 1.5, 1.75, 2.0]:
    actual_time = video_duration / speed
    time_saved = video_duration - actual_time
    print(f"  {speed}x speed: {actual_time:.1f} min (saves {time_saved:.1f} min)")

print("\n" + "=" * 70)
print("🎯 RECOMMENDATIONS")
print("=" * 70)

print("""
For Different Content Types:

  📚 Lectures/Theory:
     → 1.5x - 2.0x (Fast, good for review)
  
  💻 Coding Tutorials:
     → 1.25x - 1.5x (Moderate, can follow along)
  
  🎯 Complex Topics:
     → 1.0x - 1.25x (Normal or slightly faster)
  
  🔁 Review/Repeat Content:
     → 2.0x (Maximum speed)
  
  🆕 New/Difficult Material:
     → 1.0x (Normal speed)
""")

print("=" * 70)
print("✅ Speed control is now available in your project!")
print("=" * 70)
print()
