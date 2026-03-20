# Architecture Overview

## High-Level System Architecture

```
                                    ┌─────────────────────────────────────┐
                                    │           FRONTEND CLIENT          │
                                    │   (Web App / Mobile App / Postman) │
                                    └──────────────┬──────────────────────┘
                                                   │
                                    ┌──────────────▼──────────────────────┐
                                    │           NGINX / API GATEWAY       │
                                    │      (Load Balancer - Optional)     │
                                    └──────────────┬──────────────────────┘
                                                   │
                                    ┌──────────────▼──────────────────────┐
                                    │        DJANGO APPLICATION          │
                                    │        (Gunicorn Workers)          │
                                    │                                     │
                                    │  ┌─────────────┐  ┌─────────────┐   │
                                    │  │   REST     │  │   ADMIN    │   │
                                    │  │   API      │  │   PANEL    │   │
                                    │  └──────┬──────┘  └──────┬──────┘   │
                                    │         │                │          │
                                    │  ┌──────▼──────────────▼──────┐    │
                                    │  │      VIEW LAYER            │    │
                                    │  │  • Authentication          │    │
                                    │  │  • Quiz Management        │    │
                                    │  │  • Attempt Handling       │    │
                                    │  │  • Analytics              │    │
                                    │  └──────────────┬─────────────┘    │
                                    │                 │                  │
                                    │  ┌──────────────▼─────────────┐    │
                                    │  │     SERVICE LAYER          │    │
                                    │  • AI Quiz Generation       │    │
                                    │  • ELO Calculation         │    │
                                    │  • Performance Updates     │    │
                                    │  └──────────────┬─────────────┘    │
                                    └─────────────────┼──────────────────┘
                                                     │
                         ┌───────────────────────────┼───────────────────┐
                         │                           │                   │
              ┌──────────▼──────────┐    ┌──────────▼──────────┐  ┌───▼────┐
              │    POSTGRESQL       │    │       REDIS         │  │  AI    │
              │    DATABASE         │    │    CACHE STORE      │  │ SERVICE │
              │                     │    │                     │  │         │
              │ • Users             │    │ • Quiz Listings     │  │ Open    │
              │ • Quizzes           │    │ • Leaderboards      │  │ Router  │
              │ • Questions         │    │ • Topics Cache      │  │ (Llama) │
              │ • Attempts          │    │ • History           │  │         │
              │ • Performance       │    │ • Session Data      │  └─────────┘
              └─────────────────────┘    └─────────────────────┘
```

---

## API Request Flow

```
CLIENT                                                        DJANGO
  │                                                            │
  │  1. Request with JWT (Authorization: Bearer <token>)      │
  │───────────────────────────────────────────────────────────>│
  │                                                            │
  │                                              ┌─────────────┴─────────┐
  │                                              │   MIDDLEWARE         │
  │                                              │  • CORS              │
  │                                              │  • Authentication    │
  │                                              │  • Throttling        │
  │                                              └──────────┬───────────┘
  │                                                         │
  │  2. Authenticated Request                              │
  │<────────────────────────────────────────────────────────┤
  │                                                         │
  │                                              ┌──────────┴───────────┐
  │                                              │   VIEW LAYER         │
  │                                              │  • Validate Input    │
  │                                              │  • Check Permissions │
  │                                              │  • Process Logic     │
  │                                              └──────────┬───────────┘
  │                                                         │
  │                                              ┌──────────┴───────────┐
  │                                              │   SERVICE LAYER     │
  │                                              │  • DB Operations    │
  │                                              │  • Cache Handling    │
  │                                              │  • External APIs     │
  │                                              └──────────┬───────────┘
  │                                                         │
  │                                              ┌──────────┴───────────┐
  │                                              │   MODEL LAYER        │
  │                                              │  • ORM Queries       │
  │                                              │  • Data Validation   │
  │                                              └──────────┬───────────┘
  │                                                         │
  │  3. Response (JSON)                                    │
  │<────────────────────────────────────────────────────────┤
  │   { "id": 1, "topic": "Python", ... }                   │
```

---

## Component Details

### 1. Client Layer
- **Frontend Apps** - Web, Mobile, or API consumers
- **Postman/Newman** - For automated testing
- **Admin Panel** - Django admin interface

### 2. Web Server (Gunicorn)
- **WSGI Application** - Runs Django
- **Worker Processes** - Handles concurrent requests
- **Threads per Worker** - For I/O bound operations

### 3. Django Application

```
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO PROJECT                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              AUTHENTICATION LAYER                    │   │
│  │  • JWT Token Validation (SimpleJWT)                │   │
│  │  • User Role Checking (Admin vs User)              │   │
│  │  • Permission Classes                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ENDPOINT LAYER (Views)                  │   │
│  │                                                      │   │
│  │  /api/users/      → UserViewSet                     │   │
│  │  /api/quizzes/    → QuizViewSet                    │   │
│  │  /api/core/       → Start/Answer/Submit Views      │   │
│  │  /api/analytics/  → Stats/Leaderboard/History      │   │
│  │  /api/ai/         → AI Generation                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              BUSINESS LOGIC LAYER                   │   │
│  │                                                      │   │
│  │  • ai_service.py    → AI Quiz Generation           │   │
│  │  • services.py      → ELO & Performance Calc       │   │
│  │  • serializers.py   → Data Validation              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              DATA ACCESS LAYER                      │   │
│  │                                                      │   │
│  │  • models.py        → Database Models              │   │
│  │  • query optimization → select_related/prefetch    │   │
│  │  • caching          → Redis integration             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. Data Layer

```
┌──────────────────────┐     ┌──────────────────────┐
│     POSTGRESQL       │     │       REDIS          │
│                      │     │                      │
│ [users_customuser]  │     │ [quiz_list_1]        │
│ [quizzes_quiz]       │     │ [leaderboard]        │
│ [quizzes_question]   │ ──► │ [topics_list]        │
│ [quizzes_option]     │     │ [user_history_1]     │
│ [core_quizattempt]   │     │                      │
│ [core_answer]        │     │ TTL-based eviction   │
│ [analytics_user]    │     │                      │
│ [analytics_topic]    │     │                      │
└──────────────────────┘     └──────────────────────┘
```

### 5. External Services

```
┌─────────────────────────────────────────────────────┐
│              AI SERVICE (OpenRouter)               │
│                                                      │
│   Request: POST /api/v1/chat/completions            │
│   ├── Model: meta-llama/llama-3.1-8b-instruct      │
│   ├── Prompt: Generate quiz questions               │
│   └── Response: JSON with questions & options      │
│                                                      │
│   Fallback: Mock question generator                │
│   (when API unavailable or USE_MOCK_AI=true)        │
└─────────────────────────────────────────────────────┘
```

---

## Deployment Architecture (Railway)

```
┌─────────────────────────────────────────────────────────────┐
│                     RAILWAY PLATFORM                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  WEB SERVICE                         │   │
│  │                  (Django + Gunicorn)               │   │
│  │                                                      │   │
│  │  $ gunicorn quiz_api.wsgi --bind 0.0.0.0:$PORT    │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│           ┌─────────────┴─────────────┐                    │
│           │                           │                    │
│  ┌────────▼────────┐      ┌──────────▼────────┐          │
│  │   POSTGRESQL   │      │      REDIS        │          │
│  │   (Railway    │      │    (Railway       │          │
│  │   PostgreSQL) │      │    Redis)         │          │
│  └────────────────┘      └───────────────────┘          │
│                                                             │
│  Environment Variables:                                     │
│  • DATABASE_URL (provided by Railway)                     │
│  • REDIS_URL (provided by Railway)                        │
│  • SECRET_KEY                                              │
│  • DEBUG=False                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Internet
    │
    ▼
https://yourapp.railway.app
    │
    ├── /api/          → REST Endpoints
    ├── /admin/        → Django Admin
    └── /api/docs/    → API Docs
```

---

## CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Run tests
      - name: Run Tests
        run: |
          pip install -r requirements.txt
          newman run postman_collection.json
      
      # Deploy to Railway
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        uses: railwayapp/cli@v1
        with:
          args: up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## Key Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| JWT Auth | Stateless, scales horizontally |
| Redis Caching | Fast reads, reduces DB load |
| Separate Analytics App | Clean separation of concerns |
| AI Service Abstraction | Easy to swap providers |
| Django Admin | Quick admin panel for management |
| PostgreSQL | ACID compliance, complex queries |
| Gunicorn | Production WSGI server |
| Railway | Free tier, easy deployment |

---

## Performance Considerations

1. **Caching Strategy**
   - Quiz listings: 5 min TTL
   - Leaderboards: 1 min TTL
   - Topics: 10 min TTL

2. **Query Optimization**
   - select_related for FK lookups
   - prefetch_related for reverse FK
   - Database indexes on hot paths

3. **Rate Limiting**
   - 100 req/day anonymous
   - 1000 req/day authenticated
