# AI-Powered Quiz API

> **Tech Stack:** Django 5.1 • DRF • PostgreSQL • Redis  
> **Deployed:** Railway

## Overview

A LeetCode-like quiz API with AI-powered question generation. Admins create quiz topics, users attempt them and compete on leaderboards.

## Features

- **JWT Authentication** - Registration, login, token refresh
- **AI Quiz Generation** - OpenRouter/Llama integration with mock fallback
- **ELO Rating System** - Global + topic-specific leaderboards
- **Analytics** - Performance tracking, history, rankings
- **Performance** - Redis caching, query optimization, pagination
- **Security** - Rate limiting, input validation, answer protection

## API Endpoints

|   Method  | Endpoint                            | Description     | Auth |
|-----------|-------------------------------------|-----------------|------|
| POST      | /api/users/register/                | Register user   | No   |
| POST      | /api/token/                         | Login           | No   |
| GET       | /api/quizzes/                       | List quizzes    | Yes  |
| POST      | /api/quizzes/                       | Create AI quiz  | Admin|
| GET       | /api/quizzes/{id}/questions/        | Get questions   | Yes  |
| POST      | /api/core/quiz/{id}/start/          | Start attempt   | Yes  |
| POST      | /api/core/attempt/{id}/answer/      | Submit answer   | Yes  |
| POST      | /api/core/attempt/{id}/submit/      | Submit quiz     | Yes  |
| GET       | /api/analytics/stats/               | User stats      | Yes  |
| GET       | /api/analytics/leaderboard/         | Global rankings | Yes  |
| GET       | /api/analytics/leaderboard/{topic}/ | Topic rankings  | Yes  |

## Setup

```bash
# Local
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Docker
docker-compose up -d
python manage.py migrate
python manage.py runserver
```

## Environment Variables (.env)

```env
SECRET_KEY=secret-key
DEBUG=True
DB_NAME=quizdb
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=127.0.0.1
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
API_KEY=your-openrouter-key
USE_MOCK_AI=false
```

## Database Models

- **CustomUser** - Extended user with role (admin/user)
- **Quiz** - Topic, difficulty, created_by
- **Question/QuestionOption** - Quiz questions with options
- **QuizAttempt** - User's quiz session with score
- **UserPerformance** - Overall stats (elo, rank)
- **TopicPerformance** - Per-topic stats

## Design Decisions

1. **JWT over Sessions** - Stateless, scalable, industry standard
2. **OpenRouter with Mock** - Free AI, graceful degradation
3. **Redis Caching** - 5min quizzes, 1min leaderboards
4. **One Attempt per Quiz** - Prevents score manipulation

## Challenges Solved

1. **Answer Leakage** - Separate endpoint hiding correct answers
2. **Duplicate Topics** - Auto-increment (Python → Python 2)
3. **N+1 Queries** - select_related/prefetch_related
4. **Cache Invalidation** - Clear on every write

## AI Integration

Get free key: https://openrouter.ai/keys
- Free Llama 3.1 model: 15 req/min, 1M/month
- Mock mode: set USE_MOCK_AI=true

## Testing

```bash
newman run postman_collection.json -e postman_environment.json
# or
run_tests.bat
```

## What's Implemented

✅ JWT Auth 
✅ Role-based Permissions 
✅ AI Quiz Generation 
✅ Redis Caching 
✅ Query Optimization 
✅ Pagination 
✅ Rate Limiting 
✅ Admin Interface 
✅ ELO System 
✅ Leaderboards 
✅ History

---

**Built with clean architecture and scalability in mind**
