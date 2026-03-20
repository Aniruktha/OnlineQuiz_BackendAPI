# AI-Powered Quiz API

A comprehensive REST API for a quiz application with AI-powered question generation, built with Django and Django REST Framework.

## Features

- **User Authentication**: JWT-based registration and login
- **AI Quiz Generation**: Create quizzes dynamically using AI
- **Quiz Management**: Create, attempt, and track quizzes
- **ELO Rating System**: Competitive leaderboard
- **Analytics**: Detailed performance tracking
- **Role-based Access**: Admin and user roles

## Tech Stack

- Django 5.1
- Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)
- Redis (for caching)
- OpenRouter AI (for quiz generation)

## Setup Instructions

### Prerequisites
- Python 3.12+
- PostgreSQL
- Docker (optional)

### Local Setup

1. **Clone and navigate to project:**
```bash
cd quiz_api
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
Create a `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=quizdb
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create superuser (for admin access):**
```bash
python manage.py createsuperuser
```

7. **Run server:**
```bash
python manage.py runserver
```

### Using Docker

```bash
docker-compose up -d
```

---

## API Endpoints

### Authentication

| Endpoint | Method | Description | Auth Required |
|---------|--------|-------------|--------------|
| `/api/users/register/` | POST | Register new user | No |
| `/api/token/` | POST | Login (get JWT) | No |
| `/api/token/refresh/` | POST | Refresh JWT token | No |

**Register Request:**
```json
{
    "username": "john",
    "email": "john@example.com",
    "password": "password123"
}
```

**Login Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Quizzes

| Endpoint | Method | Description | Auth Required | Role |
|---------|--------|-------------|--------------|------|
| `/api/quizzes/` | GET | List all quizzes | Yes | All |
| `/api/quizzes/` | POST | Create AI quiz | Yes | Admin |
| `/api/quizzes/{id}/` | GET | Get quiz details | Yes | All |
| `/api/quizzes/{id}/questions/` | GET | Get questions (no answers) | Yes | All |
| `/api/quizzes/{id}/` | DELETE | Delete quiz | Yes | Admin |

**Create Quiz Request:**
```json
{
    "topic": "Python Programming",
    "question_count": 5,
    "difficulty": "medium"
}
```

**Difficulty Options:** `easy`, `medium`, `hard`

### Quiz Attempts

| Endpoint | Method | Description | Auth Required |
|---------|--------|-------------|--------------|
| `/api/core/quiz/{id}/start/` | POST | Start quiz attempt | Yes |
| `/api/core/attempt/{id}/answer/` | POST | Submit answer | Yes |
| `/api/core/attempt/{id}/submit/` | POST | Submit quiz | Yes |

**Start Quiz Response:**
```json
{
    "attempt_id": 1,
    "status": "in_progress",
    "created": true
}
```

**Submit Answer Request:**
```json
{
    "question_id": 1,
    "selected_option_id": 2
}
```

**Submit Answer Response:**
```json
{
    "is_correct": true
}
```

**Submit Quiz Response:**
```json
{
    "score": 80.0,
    "status": "completed"
}
```

### Analytics

| Endpoint | Method | Description | Auth Required |
|---------|--------|-------------|--------------|
| `/api/analytics/stats/` | GET | User performance | Yes |
| `/api/analytics/leaderboard/` | GET | Top 10 users | Yes |
| `/api/analytics/history/` | GET | Quiz history | Yes |

**User Stats Response:**
```json
{
    "total_attempts": 10,
    "avg_score": 75.5,
    "best_score": 95.0,
    "elo_points": 1250,
    "rank": "Gold"
}
```

**Leaderboard Response:**
```json
[
    {
        "rank": 1,
        "username": "player1",
        "elo_points": 1500,
        "avg_score": 92.5
    }
]
```

---

## Database Schema

### Models

1. **CustomUser**
   - username, email (unique), password
   - role (user/admin)
   - created_at

2. **Quiz**
   - topic, difficulty
   - created_by (FK to User)
   - created_at

3. **Question**
   - quiz (FK)
   - text

4. **QuestionOption**
   - question (FK)
   - option_text
   - is_correct

5. **QuizAttempt**
   - user (FK)
   - quiz (FK)
   - score, weighted_score
   - status (in_progress/completed)
   - started_at, completed_at

6. **AttemptAnswer**
   - attempt (FK)
   - question (FK)
   - selected_option (FK)
   - is_correct

7. **UserPerformance**
   - user (OneToOne)
   - total_attempts, avg_score
   - best_score, elo_points
   - rank

---

## Design Decisions

### Architecture
- **RESTful API**: Clean resource-based URLs
- **JWT Auth**: Stateless authentication suitable for APIs
- **Role-based Permissions**: Admin-only quiz creation

### Performance
- **Database Indexing**: On frequently queried fields (user+quiz, topic+elo_points)
- **Redis Caching**: Implemented for quiz listings, leaderboards, topics, and history
- **Pagination**: Configured (PAGE_SIZE=10) with manual pagination for history
- **Query Optimization**: Using select_related() and prefetch_related() to avoid N+1 queries

### Security
- **Password Validation**: Multiple validators (length, similarity, common, numeric)
- **Input Validation**: Serializers with validation
- **Answer Protection**: Correct answers never exposed to clients
- **Rate Limiting**: Configured (100/day anonymous, 1000/day authenticated)
- **CORS**: Configured for frontend integration
- **JWT Tokens**: Access token (60min) and Refresh token (7 days)

---

## AI Integration

The AI quiz generation uses **Google Gemini API** (free, no credit card needed).

### Get Your Free Gemini API Key:
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click **Create API Key**
4. Copy the key

### Add to .env:
```env
GEMINI_API_KEY=your-key-here
```

### How it works:
- When you create a quiz, the API generates unique questions
- Questions include 4 options with exactly 1 correct answer
- Supports any topic you specify

**Cost:** Gemini 2.0 Flash is FREE (15 requests/minute, 1 million requests/month)

---

## Challenges Faced

1. **Port Conflicts**: Local PostgreSQL vs Docker - resolved by using port 5433
2. **Answer Leakage**: Initially exposed correct answers - fixed by removing from serializer
3. **CORS Issues**: Added django-cors-headers for frontend integration

---

## Implementation Details

### Caching Strategy
- **Quiz Listings**: 5 minute cache
- **Leaderboards**: 1 minute cache (frequently changing)
- **Topics List**: 10 minute cache (rarely changing)
- **Quiz History**: 1 minute cache per user

### Query Optimization
- `select_related('user')` for leaderboard queries
- `prefetch_related('questions', 'options')` for quiz details
- `select_related('quiz')` for attempt queries
- Database indexes on `user+quiz`, `topic+elo_points`

### API Endpoints

| Feature | Endpoint | Method |
|---------|----------|--------|
| User Registration | `/api/users/register/` | POST |
| Login | `/api/token/` | POST |
| Refresh Token | `/api/token/refresh/` | POST |
| List Quizzes | `/api/quizzes/` | GET |
| Create Quiz (Admin) | `/api/quizzes/` | POST |
| Get Questions | `/api/quizzes/{id}/questions/` | GET |
| Start Attempt | `/api/core/quiz/{id}/start/` | POST |
| Submit Answer | `/api/core/attempt/{id}/answer/` | POST |
| Submit Quiz | `/api/core/attempt/{id}/submit/` | POST |
| User Stats | `/api/analytics/stats/` | GET |
| Topic Stats | `/api/analytics/stats/?topic=Python` | GET |
| Global Leaderboard | `/api/analytics/leaderboard/` | GET |
| Topic Leaderboard | `/api/analytics/leaderboard/Python/` | GET |
| List Topics | `/api/analytics/topics/` | GET |
| Quiz History | `/api/analytics/history/` | GET |

## Future Improvements

- Background task processing with Celery for AI generation
- API versioning
- Comprehensive test coverage
- WebSocket support for real-time features

---

## License

MIT License

---

## Senior Backend Developer Review Summary

### ✅ Implemented Features
1. **JWT Authentication** - Full implementation with registration, login, token refresh
2. **Role-based Permissions** - Admin-only quiz creation/deletion
3. **AI Integration** - OpenRouter API with mock fallback
4. **Database Models** - Complete with proper relationships and indexes
5. **Caching** - Redis caching for quizzes, leaderboards, topics, history
6. **Query Optimization** - select_related/prefetch_related throughout
7. **Pagination** - Configured with PAGE_SIZE=10
8. **Rate Limiting** - 100/day anon, 1000/day user
9. **Admin Interface** - All models registered with inline support
10. **Error Handling** - Comprehensive validation and error responses

### 📊 Performance Optimizations
- Database indexes on frequently queried fields
- Redis caching with appropriate TTLs
- Query optimization to avoid N+1 problems
- Pagination for large result sets

### 🔒 Security Features
- JWT stateless authentication
- Password validation (length, common, numeric)
- Input validation via serializers
- Answer leakage prevention
- CORS configuration
- Rate limiting
