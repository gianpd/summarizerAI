# SummarizerAI - Refactored

A modern AI-powered text summarization service built with FastAPI and Next.js App Router.

## Architecture

This project has been completely refactored from the legacy structure to a modern, scalable architecture:

### Backend (FastAPI + SQLAlchemy)
- **FastAPI 0.104.1** with async/await support
- **SQLAlchemy 2.0** with async engine and sessions
- **PostgreSQL** with asyncpg driver
- **Alembic** for database migrations
- **JWT Authentication** with secure password hashing
- **Pydantic v2** for data validation
- **Modern ML Stack**: PyTorch, Transformers, spaCy

### Frontend (Next.js App Router)
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** with shadcn/ui components
- **React Hook Form** with Zod validation
- **Axios** for API communication
- **Responsive design** with modern UI/UX

## Project Structure

```
/
├── backend/                    # FastAPI Application
│   ├── app/
│   │   ├── api/v1/            # API Routes
│   │   │   ├── endpoints/     # Individual endpoint modules
│   │   │   └── api.py         # Main API router
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py      # Settings management
│   │   │   └── security.py    # Authentication & security
│   │   ├── crud/              # Database operations (async)
│   │   ├── db/                # Database setup
│   │   │   ├── session.py     # Async session management
│   │   │   └── base_class.py  # Base model class
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── main.py           # FastAPI app entrypoint
│   ├── alembic/              # Database migrations
│   ├── tests/                # Backend tests (pytest-asyncio)
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile           # Backend container
│
├── frontend/                 # Next.js Application
│   ├── src/
│   │   ├── app/             # App Router structure
│   │   │   ├── layout.tsx   # Root layout
│   │   │   ├── page.tsx     # Home page
│   │   │   └── globals.css  # Global styles
│   │   ├── components/      # React components
│   │   │   ├── ui/         # Basic UI components
│   │   │   └── shared/     # Complex shared components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # Utility libraries
│   │   │   ├── api.ts      # API client
│   │   │   └── utils.ts    # Utility functions
│   │   ├── store/          # State management
│   │   └── types/          # TypeScript definitions
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile         # Frontend container
│
└── docker-compose.yml      # Multi-service orchestration
```

## Features

### Core Functionality
- **Text Summarization**: Paste text directly for instant summarization
- **URL Summarization**: Extract and summarize content from web articles
- **Summary History**: Browse and manage previously generated summaries
- **Real-time Processing**: Background task processing for URL content extraction

### Technical Features
- **Async Architecture**: Full async/await implementation for optimal performance
- **Type Safety**: Complete TypeScript coverage on frontend
- **Modern UI**: Responsive design with Tailwind CSS and shadcn/ui
- **Database Migrations**: Alembic for schema version control
- **Comprehensive Testing**: pytest-asyncio test suite
- **Docker Support**: Multi-service containerization
- **Security**: JWT authentication with secure password hashing

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Development Setup

1. **Clone and setup backend:**
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Setup database
cp .env.example .env  # Configure your database URL
alembic upgrade head

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Setup frontend:**
```bash
cd frontend
npm install

# Run frontend
npm run dev
```

3. **Using Docker (recommended):**
```bash
docker-compose up --build
```

### Access Points
- **Frontend**: http://localhost:12000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Summaries
- `POST /api/v1/summaries/` - Create new summary
- `GET /api/v1/summaries/` - List all summaries
- `GET /api/v1/summaries/{id}` - Get specific summary
- `DELETE /api/v1/summaries/{id}` - Delete summary

### Health
- `GET /api/v1/health` - Health check endpoint

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/summarizerdb
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
HF_TOKEN=your-huggingface-token  # Optional for advanced models
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing

### Backend Tests
```bash
cd backend
pytest -v
```

### Frontend Type Checking
```bash
cd frontend
npm run type-check
```

## Migration from Legacy

This refactoring includes:

### Backend Changes
- ✅ Migrated from Tortoise ORM to SQLAlchemy 2.0 async
- ✅ Updated to FastAPI 0.104.1 with modern patterns
- ✅ Implemented proper async database sessions
- ✅ Added Alembic for database migrations
- ✅ Modernized ML dependencies (PyTorch 2.1.1, Transformers 4.35.2)
- ✅ Added comprehensive test suite with pytest-asyncio
- ✅ Implemented JWT authentication system

### Frontend Changes
- ✅ Migrated from Pages Router to App Router (Next.js 14)
- ✅ Updated to modern React patterns with hooks
- ✅ Implemented TypeScript throughout
- ✅ Added modern UI with Tailwind CSS and shadcn/ui
- ✅ Integrated React Hook Form with Zod validation
- ✅ Added proper state management patterns

### Infrastructure Changes
- ✅ Updated Docker configuration for multi-service setup
- ✅ Added proper environment configuration
- ✅ Implemented proper CORS settings for development
- ✅ Added health check endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

