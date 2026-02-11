"""
Memey Configuration
Change these values to customize behavior.
"""

CONFIG = {
    # Detection settings
    'detection_interval': 0.3,       # Seconds between analyses
    'confidence_threshold': 0.4,     # Minimum confidence (0-1)
    
    # Trigger settings
    'emotion_hold_time': 2.0,        # Seconds to hold emotion before trigger
    'meme_cooldown': 5.0,            # Seconds between meme displays
    'meme_display_duration': 4.0,    # How long meme shows on screen
    
    # Audio
    'sound_enabled': True,
    
    # Camera
    'camera_index': 0,               # 0 = default camera
    
    # Paths
    'memes_dir': 'assets/memes',
    'sounds_dir': 'assets/sounds',
}