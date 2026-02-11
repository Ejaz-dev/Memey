"""
Emotion Detection Module
Detects facial emotions using DeepFace and MediaPipe.
"""

import cv2
import numpy as np
from deepface import DeepFace
import mediapipe as mp
import time


class EmotionDetector:
    """Real-time emotion detection using computer vision."""
    
    EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']
    
    def __init__(self, detection_interval=0.5):
        """
        Initialize the emotion detector.
        
        Args:
            detection_interval: Seconds between emotion analyses
        """
        self.detection_interval = detection_interval
        self.last_detection_time = 0
        self.last_emotion = "neutral"
        self.last_confidence = 0.0
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        print("✓ Emotion Detector initialized")
    
    def detect_emotion(self, frame):
        """
        Detect emotion from a video frame.
        
        Returns:
            Tuple of (emotion_name, confidence, full_results_dict)
        """
        current_time = time.time()
        
        # Rate limiting for performance
        if current_time - self.last_detection_time < self.detection_interval:
            return self.last_emotion, self.last_confidence, None
        
        self.last_detection_time = current_time
        
        try:
            results = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            if isinstance(results, list):
                results = results[0]
            
            emotions = results.get('emotion', {})
            dominant_emotion = results.get('dominant_emotion', 'neutral')
            confidence = emotions.get(dominant_emotion, 0) / 100.0
            
            self.last_emotion = dominant_emotion
            self.last_confidence = confidence
            
            return dominant_emotion, confidence, emotions
            
        except Exception as e:
            print(f"Detection warning: {e}")
            return self.last_emotion, self.last_confidence, None
    
    def draw_emotion_overlay(self, frame, emotion, confidence, emotions_dict=None):
        """Draw emotion information on the frame."""
        color = self._get_emotion_color(emotion)
        label = f"{emotion.upper()}: {confidence*100:.1f}%"
        
        cv2.putText(frame, label, (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        
        if emotions_dict:
            bar_y = 70
            bar_height = 20
            max_width = 150
            
            for emo, score in sorted(emotions_dict.items(), key=lambda x: -x[1]):
                bar_width = int((score / 100) * max_width)
                emo_color = self._get_emotion_color(emo)
                
                cv2.rectangle(frame, (20, bar_y), (20 + max_width, bar_y + bar_height),
                             (50, 50, 50), -1)
                cv2.rectangle(frame, (20, bar_y), (20 + bar_width, bar_y + bar_height),
                             emo_color, -1)
                cv2.putText(frame, f"{emo[:3]}", (25, bar_y + 15),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                
                bar_y += bar_height + 5
        
        return frame
    
    def _get_emotion_color(self, emotion):
        """Get BGR color for emotion."""
        colors = {
            'happy': (0, 255, 255),
            'sad': (255, 100, 100),
            'angry': (0, 0, 255),
            'surprised': (255, 0, 255),
            'fearful': (128, 0, 128),
            'disgusted': (0, 128, 0),
            'neutral': (200, 200, 200)
        }
        return colors.get(emotion, (255, 255, 255))
    
    def cleanup(self):
        """Release resources."""
        self.face_mesh.close()