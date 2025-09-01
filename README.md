# Ludus 🎲✨
Educational Bot Battles Platform

Ludus is an open-source platform where you can watch AI bots face off in classic games.  
It is designed for learning, experimentation, and fun — making game-playing AI accessible for students, educators, and hobbyists.

---

## Features
- Multiple Games: Start with Tic-Tac-Toe and Eleven Sticks, more to come.  
- Plug-in Bots: Add your own strategies in `arena_data/bots`.  
- Game-Specific Renderers: Each game has its own board and style.  
- Leaderboards: Track bot performance over matches.  
- Internationalization (i18n): English + Portuguese support.  
- Backup & Restore: Save your arena data easily.  

---

## Project Structure
frontend/ → Web app (HTML, CSS, JS, renderers)
arena/ → Python backend (FastAPI + Uvicorn)
arena_data/ → Game configs and bots


---

## Installation

### Requirements
- Python 3.11+
- Node.js (if customizing frontend)
- pipenv / venv recommended

### Setup
```bash
git clone https://github.com/YOUR_USERNAME/ludus.git
cd ludus

# Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run server
python -m arena.start_server
Then open http://localhost:8000 in your browser.
