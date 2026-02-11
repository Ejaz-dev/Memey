"""
Meme Manager Module
Handles loading and displaying emotion-based memes.
"""

import os
import random
from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import Label
from threading import Thread


class MemeManager:
    """Manages meme images organized by emotion categories."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    def __init__(self, memes_directory="assets/memes"):
        """
        Initialize the meme manager.
        
        Args:
            memes_directory: Path to directory containing emotion subdirectories
        """
        self.memes_dir = Path(memes_directory)
        self.meme_cache = {}
        self.current_window = None
        self.is_displaying = False
        
        self._load_meme_library()
        print(f"✓ Meme Manager initialized with {self._count_memes()} memes")
    
    def _load_meme_library(self):
        """Scan meme directory and cache file paths by emotion."""
        if not self.memes_dir.exists():
            print(f"⚠ Creating meme directory: {self.memes_dir}")
            self.memes_dir.mkdir(parents=True, exist_ok=True)
        
        for emotion_dir in self.memes_dir.iterdir():
            if emotion_dir.is_dir():
                emotion = emotion_dir.name.lower()
                memes = [
                    f for f in emotion_dir.iterdir()
                    if f.suffix.lower() in self.SUPPORTED_FORMATS
                ]
                self.meme_cache[emotion] = memes
                
                if not memes:
                    print(f"  ⚠ No memes found for: {emotion}")
    
    def _count_memes(self):
        """Count total memes across all emotions."""
        return sum(len(memes) for memes in self.meme_cache.values())
    
    def get_random_meme(self, emotion):
        """Get a random meme path for the given emotion."""
        emotion = emotion.lower()
        
        if emotion in self.meme_cache and self.meme_cache[emotion]:
            return random.choice(self.meme_cache[emotion])
        
        # Fallback to neutral
        if 'neutral' in self.meme_cache and self.meme_cache['neutral']:
            return random.choice(self.meme_cache['neutral'])
        
        return None
    
    def display_meme(self, emotion, duration=3.0):
        """
        Display a meme popup for the given emotion.
        
        Args:
            emotion: Emotion to display meme for
            duration: How long to show the meme (seconds)
        """
        meme_path = self.get_random_meme(emotion)
        
        if not meme_path:
            print(f"No meme available for: {emotion}")
            return
        
        self.close_current_display()
        
        # Display in new thread to not block main loop
        display_thread = Thread(
            target=self._display_window,
            args=(meme_path, emotion, duration)
        )
        display_thread.start()
    
    def _display_window(self, meme_path, emotion, duration):
        """Create and show meme window."""
        self.is_displaying = True
        
        try:
            root = tk.Tk()
            root.title(f"😊 {emotion.upper()} DETECTED!")
            
            # Load and resize image
            img = Image.open(meme_path)
            
            # Resize to fit screen
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            max_width = int(screen_width * 0.5)
            max_height = int(screen_height * 0.5)
            
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Convert for Tkinter
            from PIL import ImageTk
            photo = ImageTk.PhotoImage(img)
            
            # Create label with image
            label = Label(root, image=photo)
            label.image = photo
            label.pack()
            
            # Add emotion text
            emotion_label = Label(
                root,
                text=f"You look {emotion}!",
                font=("Arial", 20, "bold"),
                fg=self._get_emotion_color_hex(emotion)
            )
            emotion_label.pack(pady=10)
            
            # Center window
            root.update_idletasks()
            x = (screen_width - root.winfo_width()) // 2
            y = (screen_height - root.winfo_height()) // 2
            root.geometry(f"+{x}+{y}")
            
            self.current_window = root
            
            # Auto-close after duration
            root.after(int(duration * 1000), root.destroy)
            root.mainloop()
            
        except Exception as e:
            print(f"Error displaying meme: {e}")
        finally:
            self.is_displaying = False
            self.current_window = None
    
    def close_current_display(self):
        """Close currently displayed meme window."""
        if self.current_window:
            try:
                self.current_window.destroy()
            except:
                pass
            self.current_window = None
    
    def _get_emotion_color_hex(self, emotion):
        """Get hex color for emotion."""
        colors = {
            'happy': '#FFD700',
            'sad': '#4169E1',
            'angry': '#FF4444',
            'surprised': '#FF69B4',
            'fearful': '#8B008B',
            'disgusted': '#228B22',
            'neutral': '#808080'
        }
        return colors.get(emotion.lower(), '#FFFFFF')
    
    def list_available_emotions(self):
        """Return list of emotions that have memes."""
        return [e for e, memes in self.meme_cache.items() if memes]