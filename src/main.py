"""
Memey - Emotion-Based Meme Generator
Main application that ties everything together.
"""

import cv2
import time
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.emotion_detector import EmotionDetector
from src.meme_manager import MemeManager
from src.audio_player import AudioPlayer


class Memey:
    """Main application class."""
    
    def __init__(self):
        """Initialize Memey."""
        print("\n" + "="*50)
        print("🎭 MEMEY - Emotion Meme Generator")
        print("="*50 + "\n")
        
        # Settings
        self.detection_interval = 0.3
        self.emotion_hold_time = 2.0      # Seconds to hold emotion before trigger
        self.meme_cooldown = 5.0          # Seconds between memes
        self.meme_display_duration = 4.0  # How long meme shows
        self.confidence_threshold = 0.4   # Minimum confidence
        self.sound_enabled = True
        
        # Initialize components
        self.detector = EmotionDetector(detection_interval=self.detection_interval)
        self.meme_manager = MemeManager(memes_directory="assets/memes")
        self.audio_player = AudioPlayer(sounds_directory="assets/sounds")
        
        # State tracking
        self.current_emotion = "neutral"
        self.emotion_start_time = None
        self.meme_triggered = False
        self.last_meme_time = 0
        
        # Camera
        self.camera = None
        
        print("\n✓ Memey is ready!")
        print("\nControls:")
        print("  ESC - Quit")
        print("  R   - Reset emotion timer")
        print("  M   - Manually trigger meme")
        print("  S   - Toggle sound\n")
    
    def run(self):
        """Main application loop."""
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        
        if not self.camera.isOpened():
            print("❌ Error: Could not open camera")
            print("   Make sure your webcam is connected.")
            return
        
        print("📷 Camera started!")
        print("="*50 + "\n")
        
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Mirror the frame
                frame = cv2.flip(frame, 1)
                
                # Detect emotion
                emotion, confidence, emotions_dict = self.detector.detect_emotion(frame)
                
                # Draw overlay
                frame = self.detector.draw_emotion_overlay(
                    frame, emotion, confidence, emotions_dict
                )
                
                # Process emotion
                self._process_emotion(emotion, confidence)
                
                # Draw status
                self._draw_status(frame)
                
                # Display frame
                cv2.imshow('Memey - Press ESC to quit', frame)
                
                # Handle keyboard
                key = cv2.waitKey(1) & 0xFF
                if not self._handle_key(key, emotion):
                    break
                    
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        finally:
            self.cleanup()
    
    def _process_emotion(self, emotion, confidence):
        """Process detected emotion and trigger meme if needed."""
        current_time = time.time()
        
        # Check confidence threshold
        if confidence < self.confidence_threshold:
            emotion = "neutral"
        
        # Check if emotion changed
        if emotion != self.current_emotion:
            self.current_emotion = emotion
            self.emotion_start_time = current_time
            self.meme_triggered = False
            return
        
        # Initialize start time
        if self.emotion_start_time is None:
            self.emotion_start_time = current_time
            return
        
        emotion_duration = current_time - self.emotion_start_time
        cooldown_ok = (current_time - self.last_meme_time) >= self.meme_cooldown
        
        # Trigger conditions
        if (emotion != "neutral" and 
            emotion_duration >= self.emotion_hold_time and
            not self.meme_triggered and
            cooldown_ok):
            
            self._trigger_meme(emotion)
    
    def _trigger_meme(self, emotion):
        """Trigger meme display and audio."""
        print(f"\n🎉 {emotion.upper()} detected! Showing meme...")
        
        # Show meme
        self.meme_manager.display_meme(
            emotion, 
            duration=self.meme_display_duration
        )
        
        # Play sound
        if self.sound_enabled:
            self.audio_player.play_emotion_sound(emotion)
        
        self.meme_triggered = True
        self.last_meme_time = time.time()
    
    def _draw_status(self, frame):
        """Draw status information on frame."""
        height, width = frame.shape[:2]
        current_time = time.time()
        
        # Status box
        cv2.rectangle(frame, (width-260, 10), (width-10, 110), (0, 0, 0), -1)
        cv2.rectangle(frame, (width-260, 10), (width-10, 110), (100, 100, 100), 2)
        
        # Emotion hold progress
        if self.emotion_start_time and self.current_emotion != "neutral":
            hold_time = current_time - self.emotion_start_time
            progress = min(hold_time / self.emotion_hold_time, 1.0)
            
            # Progress bar
            bar_width = 230
            cv2.rectangle(frame, (width-250, 30), (width-20, 50), (50, 50, 50), -1)
            cv2.rectangle(frame, (width-250, 30), 
                         (width-250 + int(bar_width * progress), 50), (0, 255, 0), -1)
            
            cv2.putText(frame, f"Hold: {hold_time:.1f}s / {self.emotion_hold_time}s",
                       (width-250, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            cv2.putText(frame, "Waiting for emotion...",
                       (width-250, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Cooldown status
        cooldown_remaining = max(0, self.meme_cooldown - (current_time - self.last_meme_time))
        if cooldown_remaining > 0 and self.last_meme_time > 0:
            cv2.putText(frame, f"Cooldown: {cooldown_remaining:.1f}s",
                       (width-250, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        else:
            cv2.putText(frame, "Ready!",
                       (width-250, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    def _handle_key(self, key, current_emotion):
        """Handle keyboard input. Returns False to exit."""
        if key == 27:  # ESC
            return False
        elif key == ord('r') or key == ord('R'):
            self.emotion_start_time = None
            self.meme_triggered = False
            print("⏱ Timer reset")
        elif key == ord('m') or key == ord('M'):
            emotion = current_emotion if current_emotion != "neutral" else "happy"
            self._trigger_meme(emotion)
        elif key == ord('s') or key == ord('S'):
            self.sound_enabled = not self.sound_enabled
            status = "ON" if self.sound_enabled else "OFF"
            print(f"🔊 Sound: {status}")
            if not self.sound_enabled:
                self.audio_player.stop()
        
        return True
    
    def cleanup(self):
        """Clean up resources."""
        print("\n🧹 Cleaning up...")
        
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        
        self.detector.cleanup()
        self.meme_manager.close_current_display()
        self.audio_player.cleanup()
        
        print("👋 Goodbye!\n")


def main():
    """Entry point."""
    app = Memey()
    app.run()


if __name__ == "__main__":
    main()