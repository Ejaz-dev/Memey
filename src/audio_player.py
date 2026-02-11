"""
Audio Player Module
Handles playing emotion-specific sounds.
"""

from pathlib import Path
import pygame


class AudioPlayer:
    """Manages audio playback for emotion-based sounds."""
    
    SUPPORTED_FORMATS = {'.mp3', '.wav', '.ogg'}
    
    def __init__(self, sounds_directory="assets/sounds"):
        """
        Initialize the audio player.
        
        Args:
            sounds_directory: Path to directory containing sound files
        """
        self.sounds_dir = Path(sounds_directory)
        self.sound_cache = {}
        self.is_playing = False
        
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        self._load_sound_library()
        print(f"✓ Audio Player initialized with {len(self.sound_cache)} sounds")
    
    def _load_sound_library(self):
        """Scan sounds directory and cache file paths by emotion."""
        if not self.sounds_dir.exists():
            print(f"⚠ Creating sounds directory: {self.sounds_dir}")
            self.sounds_dir.mkdir(parents=True, exist_ok=True)
            return
        
        for sound_file in self.sounds_dir.iterdir():
            if sound_file.suffix.lower() in self.SUPPORTED_FORMATS:
                # Use filename (without extension) as emotion key
                emotion = sound_file.stem.lower()
                self.sound_cache[emotion] = sound_file
    
    def play_emotion_sound(self, emotion, loop=False):
        """
        Play the sound associated with an emotion.
        
        Args:
            emotion: Emotion name (should match filename)
            loop: Whether to loop the sound
        """
        emotion = emotion.lower()
        
        if emotion not in self.sound_cache:
            # Try partial match
            for cached_emotion in self.sound_cache:
                if emotion in cached_emotion or cached_emotion in emotion:
                    emotion = cached_emotion
                    break
            else:
                return  # No sound found
        
        sound_path = self.sound_cache[emotion]
        
        try:
            self.stop()
            pygame.mixer.music.load(str(sound_path))
            loops = -1 if loop else 0
            pygame.mixer.music.play(loops)
            self.is_playing = True
        except Exception as e:
            print(f"Error playing sound: {e}")
    
    def stop(self):
        """Stop currently playing audio."""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
        except:
            pass
    
    def set_volume(self, volume):
        """
        Set playback volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    
    def is_sound_playing(self):
        """Check if audio is currently playing."""
        return pygame.mixer.music.get_busy()
    
    def cleanup(self):
        """Clean up pygame mixer."""
        self.stop()
        pygame.mixer.quit()