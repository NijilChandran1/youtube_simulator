# Backend - EPG Training Feedback Loop API

FastAPI-based backend service for analyzing training videos and providing AI-powered feedback using Google Gemini.

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **FFmpeg**: Required for video processing
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`
- **Google Cloud API Key**: For Gemini AI integration

## 🚀 Quick Start

### 1. Set Up Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create or update the `.env` file in the `backend` directory:

```env
# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Google Cloud / Vertex AI
GOOGLE_API_KEY=your_actual_api_key_here
GOOGLE_CLOUD_PROJECT=your_project_id

# Database
DATABASE_URL=sqlite:///./data/training.db

# Storage
UPLOAD_DIR=uploads/videos
MAX_VIDEO_SIZE_MB=500
ALLOWED_VIDEO_FORMATS=["mp4","webm","mov"]

# Security (for future use)
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> [!IMPORTANT]
> Replace `your_actual_api_key_here` with your actual Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### 4. Initialize Database

```bash
# From the backend directory
python -m app.init_db
```

### 5. Start the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the configured settings
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and settings
│   ├── database.py          # Database connection setup
│   ├── init_db.py           # Database initialization script
│   ├── models/              # SQLAlchemy database models
│   ├── routes/              # API route handlers
│   │   ├── video_analysis.py
│   │   ├── events.py
│   │   └── sessions.py
│   ├── schemas/             # Pydantic schemas for validation
│   ├── services/            # Business logic and AI services
│   └── utils/               # Utility functions
├── data/                    # SQLite database storage
├── uploads/                 # Uploaded video files
├── venv/                    # Virtual environment
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔌 API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

### Video Analysis
- `POST /api/analyze` - Upload and analyze a training video
- `GET /api/analysis/{session_id}` - Get analysis results

### Events
- `POST /api/events` - Log user interaction events
- `GET /api/events/{session_id}` - Get events for a session

### Sessions
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{session_id}` - Get session details

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test files
python test_analysis.py
python test_data_flow.py
python test_imports.py
python test_session_flow.py
```

### Code Style

The project follows standard Python conventions:
- PEP 8 style guide
- Type hints for function signatures
- Docstrings for modules and functions

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | Server host address | `0.0.0.0` |
| `API_PORT` | Server port | `8000` |
| `DEBUG` | Enable debug mode | `True` |
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `GOOGLE_CLOUD_PROJECT` | GCP project ID | Optional |
| `DATABASE_URL` | Database connection string | `sqlite:///./data/training.db` |
| `UPLOAD_DIR` | Video upload directory | `uploads/videos` |
| `MAX_VIDEO_SIZE_MB` | Maximum video file size | `500` |

### CORS Configuration

By default, CORS is configured to allow all origins for development. For production:

```python
# In app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📦 Dependencies

Core dependencies:
- **FastAPI** (0.109.2) - Modern web framework
- **Uvicorn** (0.27.1) - ASGI server
- **SQLAlchemy** (2.0.27) - Database ORM
- **Pydantic** (2.6.1) - Data validation
- **google-genai** (0.2.0) - Google Gemini AI SDK
- **opencv-python** (4.9.0.80) - Video processing
- **ffmpeg-python** (0.2.0) - FFmpeg wrapper

See `requirements.txt` for complete list.

## 🐛 Troubleshooting

### Common Issues

**1. FFmpeg not found**
```bash
# Verify FFmpeg installation
ffmpeg -version

# If not installed, install it based on your OS (see Prerequisites)
```

**2. Database errors**
```bash
# Reinitialize the database
python -m app.init_db
```

**3. Import errors**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**4. Port already in use**
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

**5. Google API authentication errors**
- Verify your API key is correct in `.env`
- Check API key permissions in Google Cloud Console
- Ensure billing is enabled for your GCP project

## 📝 Notes

- The application uses SQLite for development. For production, consider PostgreSQL or MySQL.
- Video files are stored locally in the `uploads/` directory.
- The API uses Google Gemini for AI-powered video analysis.
- All timestamps and events are logged to the database for analytics.

## 🔗 Related Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
