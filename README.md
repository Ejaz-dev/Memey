# 🎭 Memey

A real-time facial emotion detection app that displays memes based on your mood!

## Features
- Real-time webcam emotion detection
- 7 emotion categories: happy, sad, angry, surprised, fearful, disgusted, neutral
- Customizable meme library
- Optional sound effects
- Configurable trigger thresholds

## Installation

1. Clone the repo:
```bash
   git clone https://github.com/YOUR-USERNAME/memey.git
   cd memey
```

2. Create virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Add memes to `assets/memes/<emotion>/` folders

5. Run:
```bash
   python src/main.py
```

## Controls
| Key | Action |
|-----|--------|
| ESC | Quit |
| R | Reset emotion timer |
| M | Manually trigger meme |
| S | Toggle sound |

## Adding Memes
Place images (.jpg, .png, .gif) in the appropriate folder:
- `assets/memes/happy/`
- `assets/memes/sad/`
- `assets/memes/angry/`
- `assets/memes/surprised/`
- `assets/memes/fearful/`
- `assets/memes/disgusted/`
- `assets/memes/neutral/`

## Adding Sounds
Place audio files (.mp3, .wav, .ogg) in `assets/sounds/`:
- Name them by emotion: `happy.mp3`, `sad.wav`, etc.

## Configuration
Edit `src/config.py` to customize:
- Detection sensitivity
- Trigger timing
- Sound settings

## License
MIT