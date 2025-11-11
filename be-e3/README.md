# E3 Backend API

FastAPI backend with Supabase for managing agents, drivers, and test call conversations.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your Supabase credentials and API key.

3. Run database migrations:
Execute the SQL in `app/database/migrations.sql` in your Supabase SQL editor.

4. Start the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

All endpoints require an API key passed via the `X-API-Key` header.

