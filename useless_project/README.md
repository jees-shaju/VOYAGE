# NOTHING — The Ultimate Inaction Simulator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-092E20.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Entry for the Useless Software Competition**  
> An intensely competitive web game where the singular objective is to literally **do nothing**. 

---

## 🕹️ Game Overview & Mechanics

As soon as the page loads, the timer starts ticking at `0.00s`. The site actively monitors the window for any input action:
- 🖱️ **Mouse Movement** (`mousemove`)
- ⌨️ **Keyboard Interaction** (`keydown`)
- 👆 **Click & Context Menu Events** (`click`, `contextmenu`, `mousedown`)
- 📜 **Scrolling & Wheel** (`scroll`, `wheel`)
- 🔀 **Tab Switching & Blur** (`visibilitychange`, `blur`)
- 📱 **Touch Gestures** (`touchstart`)

The millisecond you commit any of these actions, the timer freezes instantly, triggering a **GAME OVER** modal with the exact failure reason, your total seconds wasted, and an input to submit your score to the global **"Hall of Utter Waste"** leaderboard.

---

## 🛠️ Tech Stack

- **Backend:** Django 5+ / Python 3.12
- **Database:** SQLite (default) / PostgreSQL support via `DATABASE_URL`
- **Frontend:** Vanilla HTML5, CSS3 (Dark Neon Monospace Terminal Theme), JavaScript (ES6+, Web Audio API synthesized sound effects)
- **Deployment:** Production-ready with `whitenoise`, `gunicorn`, `Dockerfile`, `Procfile`, and environment variable support.

---

## 🚀 Quickstart (Local Development)

### 1. Clone & Navigate to Project
```bash
git clone <repository-url>
cd useless_project
```

### 2. (Optional) Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations core
python manage.py migrate
```

### 5. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and visit: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**  
*(Remember: Do not touch your mouse or keyboard when the page loads!)*

---

## 🧪 Running Automated Tests

To execute the test suite validating model ordering, 100-row database cap eviction, and API endpoints:
```bash
python manage.py test core
```

---

## 📡 API Endpoints

### 1. Leaderboard
- **Route:** `GET /api/leaderboard/`
- **Response:**
  ```json
  [
    {
      "username": "ZenMaster",
      "seconds_wasted": 142.85,
      "created_at": "2026-09-12 04:20"
    }
  ]
  ```

### 2. Submit Score
- **Route:** `POST /api/submit/`
- **Payload:**
  ```json
  {
    "username": "Procrastinator",
    "seconds": 23.45
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Score submitted successfully!",
    "score": {
      "username": "Procrastinator",
      "seconds_wasted": 23.45
    }
  }
  ```
> **Note:** The database enforces a strict maximum cap of 100 records. Once the 101st score is saved, the row with the lowest `seconds_wasted` is automatically evicted.

---

## ☁️ Deployment Instructions

### 1. Render / Railway / Heroku (Recommended 1-Click)
This repository includes a `Procfile` and `requirements.txt` ready for PaaS platforms.
1. Connect your Git repository to **Render** or **Railway**.
2. Set Environment Variables:
   - `DEBUG=False`
   - `SECRET_KEY=your-production-secret-key`
   - `ALLOWED_HOSTS=.onrender.com,.railway.app,yourdomain.com`
3. Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Start Command: `gunicorn nothing_game.wsgi:application`

### 2. Docker Deployment
```bash
docker build -t nothing-game .
docker run -p 8000:8000 -e DEBUG=False -e ALLOWED_HOSTS=* nothing-game
```
Or via Docker Compose:
```bash
docker compose up -d
```

---

## 📜 License
MIT License. Created for the Useless Software League.
