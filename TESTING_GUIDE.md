# Complete Postman Testing Guide for Quiz API

> **Created by:** Senior Backend Developer  
> **For:** Complete Beginner  
> **API Style:** LeetCode-like (Admin creates quizzes, Users take them)

---

## 🚀 Quick Start: First Time Manual Testing

Follow these steps in order for your first test. After this, you can run automated tests.

### Step 1: Make Sure Server is Running
```cmd
cd c:\Users\aniruktha\Documents\onlineQuizz\quiz_api
python manage.py runserver
```
> Server runs at: http://127.0.0.1:8000

### Step 2: Clear Database (Fresh Start)
```cmd
python manage.py flush --noinput
```

### Step 3: Register Admin User (First user becomes admin automatically!)
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/users/register/ |
| Body | `{"username": "admin", "email": "admin@quiz.com", "password": "admin123"}` |

### Step 4: Login as Admin
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/token/ |
| Body | `{"username": "admin", "password": "admin123"}` |
| Save | Copy `access` token as `admin_token` |

### Step 5: Create First Quiz (Topic: Python)
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/quizzes/ |
| Auth | Bearer `admin_token` |
| Body | `{"topic": "Python", "question_count": 3, "difficulty": "easy"}` |
| Save | Copy `id` as `quiz_id` |

### Step 6: Create Second Quiz (Same Topic - Will Auto-Increment!)
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/quizzes/ |
| Auth | Bearer `admin_token` |
| Body | `{"topic": "Python", "question_count": 3, "difficulty": "medium"}` |
| Result | Topic will be `"Python 2"` automatically! ✅ |

### Step 7: Create Third Quiz (JavaScript)
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/quizzes/ |
| Auth | Bearer `admin_token` |
| Body | `{"topic": "JavaScript", "question_count": 3, "difficulty": "easy"}` |

### Step 8: Register Regular User
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/users/register/ |
| Body | `{"username": "testuser", "email": "testuser@quiz.com", "password": "testpass123"}` |

### Step 9: Login as Regular User
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/token/ |
| Body | `{"username": "testuser", "password": "testpass123"}` |
| Save | Copy `access` token as `user_token` |

### Step 10: List Quizzes
| Field | Value |
|-------|-------|
| Method | GET |
| URL | http://127.0.0.1:8000/api/quizzes/ |
| Auth | Bearer `user_token` |
| Result | Should see Python, Python 2, JavaScript ✅ |

### Step 11: Get Quiz Questions
| Field | Value |
|-------|-------|
| Method | GET |
| URL | http://127.0.0.1:8000/api/quizzes/1/questions/ |
| Auth | Bearer `user_token` |

### Step 12: Start Quiz Attempt
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/core/quiz/1/start/ |
| Auth | Bearer `user_token` |
| Body | `{}` |
| Save | Copy `id` as `attempt_id` |

### Step 13: Submit Answer
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/core/attempt/1/answer/ |
| Auth | Bearer `user_token` |
| Body | `{"question_id": 1, "selected_option_id": 1}` |

### Step 14: Submit Quiz
| Field | Value |
|-------|-------|
| Method | POST |
| URL | http://127.0.0.1:8000/api/core/attempt/1/submit/ |
| Auth | Bearer `user_token` |
| Body | `{}` |

### Step 15: Check Stats
| Field | Value |
|-------|-------|
| Method | GET |
| URL | http://127.0.0.1:8000/api/analytics/stats/ |
| Auth | Bearer `user_token` |

### Step 16: Check Leaderboard
| Field | Value |
|-------|-------|
| Method | GET |
| URL | http://127.0.0.1:8000/api/analytics/leaderboard/ |
| Auth | Bearer `user_token` |

---

## 🎯 After Manual Testing: Run Automated Tests

Once you've done manual testing, run automated tests:

```cmd
cd quiz_api
newman run postman_collection.json -e postman_environment.json
```

---

## What is this API about?

Think of this like **LeetCode**:
- **Admin** creates quizzes (like problems) on topics like "Python", "JavaScript", etc.
- **Users** can take any quiz and see their rankings
- Each **topic** has its own leaderboard (like LeetCode problem sets)

---

## Prerequisites

Before starting, make sure:
1. ✅ **Docker Desktop is running** (PostgreSQL & Redis)
2. ✅ **Postman is installed**
3. ✅ **Server is running** (`python manage.py runserver` in quiz_api folder)

---

## Step 1: Start the Backend Server

1. Open **Command Prompt** (cmd)
2. Navigate to the project:
   ```cmd
   cd c:\Users\aniruktha\Documents\onlineQuizz\quiz_api
   ```
3. Run the server:
   ```cmd
   python manage.py runserver
   ```
4. **Keep this window open!** Server runs at `http://127.0.0.1:8000`

---

## Step 2: Get Your Free Gemini API Key (IMPORTANT!)

For AI quiz generation to work:

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with Google
3. Click **"Create API Key"**
4. Copy your key (looks like: `AIzaSy...`)
5. Open `quiz_api\.env` in VS Code
6. Replace the placeholder:
   ```
   GEMINI_API_KEY=AIzaSyCxxxxxxxxxxxxxxxxxxxx
   ```
7. **Restart the server** (close cmd, run again)

---

## Step 3: Set Up Postman Environment

This makes testing much easier!

### Create Environment:
1. In Postman, click **"Environments"** (top right 🔽)
2. Click **"Manage Environments"**
3. Click **"+"** 
4. Name: `Quiz API Dev`

### Add Variables:
Add these exact variables:

| Variable | Initial Value | Current Value |
|----------|--------------|---------------|
| `base_url` | http://127.0.0.1:8000 | http://127.0.0.1:8000 |
| `access_token` | (empty) | (empty) |
| `refresh_token` | (empty) | (empty) |
| `quiz_id` | (empty) | (empty) |
| `attempt_id` | (empty) | (empty) |

5. Click **Save**
6. Select `Quiz API Dev` from dropdown

---

## Step 4: Create Your First Admin User

Since only admins can create quizzes, let's create one:

### Register Admin User:
1. New tab in Postman
2. **Method:** `POST`
3. **URL:** `{{base_url}}/api/users/register/`
4. **Body** (JSON):
   ```json
   {
       "username": "admin",
       "email": "admin@quiz.com",
       "password": "admin123"
   }
   ```
5. Click **Send**
6. Should return: `"message": "User created successfully"`

### Make Admin (Important!):
1. Open **new command prompt** (keep server running)
2. Run:
   ```cmd
   cd c:\Users\aniruktha\Documents\onlineQuizz\quiz_api
   python manage.py shell
   ```
3. In shell, type:
   ```python
   from users.models import CustomUser
   u = CustomUser.objects.get(username='admin')
   u.is_staff = True
   u.is_superuser = True
   u.save()
   print("Admin created!")
   exit()
   ```
4. ✅ Admin user is ready!

---

## Step 5: Login as Admin

1. In Postman, new tab
2. **Method:** `POST`
3. **URL:** `{{base_url}}/api/token/`
4. **Body:**
   ```json
   {
       "username": "admin",
       "password": "admin123"
   }
   ```
5. Click **Send**
6. Copy the `access` token value
7. In the request, go to **Authorization** tab
8. Type: `Bearer`
9. Paste token in **Token** field

---

## Step 6: Admin - Create Quizzes (Topics)

Now let's create quizzes on different topics (like LeetCode problem sets):

### Create Python Quiz:
1. **Method:** `POST`
2. **URL:** `{{base_url}}/api/quizzes/`
3. **Authorization:** Bearer token (from admin login)
4. **Body:**
   ```json
   {
       "topic": "Python",
       "question_count": 3,
       "difficulty": "easy"
   }
   ```
5. Click **Send**
6. Copy the `id` from response (e.g., `"id": 1`)
7. In environment, set `quiz_id` = `1`

### Create JavaScript Quiz:
Repeat with:
```json
{
    "topic": "JavaScript",
    "question_count": 3,
    "difficulty": "medium"
}
```

### Create Data Structures Quiz:
```json
{
    "topic": "Data Structures",
    "question_count": 3,
    "difficulty": "hard"
}
```

✅ **Now you have 3 topics: Python, JavaScript, Data Structures**

---

## Step 7: Register a Regular User

Now let's create a regular user who will take quizzes:

1. **Method:** `POST`
2. **URL:** `{{base_url}}/api/users/register/`
3. **Body:**
   ```json
   {
       "username": "john_doe",
       "email": "john@example.com",
       "password": "password123"
   }
   ```
4. Click **Send**

---

## Step 8: Login as Regular User

1. **Method:** `POST`
2. **URL:** `{{base_url}}/api/token/`
3. **Body:**
   ```json
   {
       "username": "john_doe",
       "password": "password123"
   }
   ```
4. **Send** - Copy the new `access` token
5. Update Authorization with this new token (regular user, not admin!)

---

## Step 9: List All Quizzes (Browse Problems)

1. **Method:** `GET`
2. **URL:** `{{base_url}}/api/quizzes/`
3. **Authorization:** Bearer token (regular user)
4. **Send**
5. ✅ See all available quizzes (Python, JavaScript, Data Structures)

---

## Step 10: Get Quiz Questions

1. **Method:** `GET`
2. **URL:** `{{base_url}}/api/quizzes/{{quiz_id}}/questions/`
3. **Authorization:** Bearer token
4. **Send**
5. Copy a `question_id` and an `option_id` for testing

---

## Step 11: Start Quiz Attempt

1. **Method:** `POST`
2. **URL:** `{{base_url}}/api/core/quiz/{{quiz_id}}/start/`
3. **Authorization:** Bearer token
4. **Body:** leave empty `{}`
5. **Send**
6. Copy `attempt_id` to environment

---

## Step 12: Submit Answer

1. **Method:** `POST`
2. **URL:** `{{base_url}}/api/core/attempt/{{attempt_id}}/answer/`
3. **Authorization:** Bearer token
4. **Body:**
   ```json
   {
       "question_id": 1,
       "option_id": 1
   }
   ```
5. **Send**
6. Response shows `"is_correct": true` or `false`

---

## Step 13: Submit Quiz (Complete)

1. **Method:** `POST`
2. **URL:** `{{base_url}}/api/core/attempt/{{attempt_id}}/submit/`
3. **Authorization:** Bearer token
4. **Body:** empty
5. **Send**
6. **Response:**
   ```json
   {
       "score": 100,
       "total_questions": 3,
       "correct_answers": 3,
       "status": "completed"
   }
   ```
7. ✅ ELO points updated for both overall AND topic!

---

## Step 14: View User Stats

### Overall Stats:
1. **Method:** `GET`
2. **URL:** `{{base_url}}/api/analytics/stats/`
3. **Authorization:** Bearer token
4. **Send**
5. Response:
   ```json
   {
       "total_attempts": 1,
       "avg_score": 100,
       "best_score": 100,
       "elo_points": 1032,
       "rank": "Novice"
   }
   ```

### Topic-Specific Stats (e.g., Python):
1. **Method:** `GET`
2. **URL:** `{{base_url}}/api/analytics/stats/?topic=Python`
3. **Authorization:** Bearer token
4. **Send**

---

## Step 15: View Leaderboards (Like LeetCode!)

### Global Leaderboard (All Topics):
1. **Method:** `GET`
2. **URL:** `{{base_url}}/api/analytics/leaderboard/`
3. **Authorization:** Bearer token
4. **Send**

### Python Topic Leaderboard:
1. **Method:** `GET`
2. **URL:** `{{base_url}}/api/analytics/leaderboard/Python/`
3. **Authorization:** Bearer token
4. **Send**
5. ✅ See rankings for Python topic only!

### JavaScript Leaderboard:
```
{{base_url}}/api/analytics/leaderboard/JavaScript/
```

---

## Step 16: List All Topics

1. **Method:** `GET`
2. **URL:** `{{base_url}}/api/analytics/topics/`
3. **Authorization:** Bearer token
4. **Send**
5. Response: `{"topics": ["Python", "JavaScript", "Data Structures"]}`

---

## Step 17: View Quiz History

### All History:
1. **Method:** `GET`
2. **URL:** `{{base_url}}/api/analytics/history/`
3. **Authorization:** Bearer token
4. **Send**

### Filter by Topic:
```
{{base_url}}/api/analytics/history/?topic=Python
```

---

## Quick Reference: All Endpoints

| Action | Method | URL | Auth |
|--------|--------|-----|------|
| Register | POST | `/api/users/register/` | No |
| Login | POST | `/api/token/` | No |
| Refresh Token | POST | `/api/token/refresh/` | No |
| List Quizzes | GET | `/api/quizzes/` | User |
| Create Quiz | POST | `/api/quizzes/` | **Admin** |
| Get Questions | GET | `/api/quizzes/{id}/questions/` | User |
| Start Quiz | POST | `/api/core/quiz/{id}/start/` | User |
| Submit Answer | POST | `/api/core/attempt/{id}/answer/` | User |
| Submit Quiz | POST | `/api/core/attempt/{id}/submit/` | User |
| User Stats | GET | `/api/analytics/stats/` | User |
| Topic Stats | GET | `/api/analytics/stats/?topic=Python` | User |
| Global Leaderboard | GET | `/api/analytics/leaderboard/` | User |
| Python Leaderboard | GET | `/api/analytics/leaderboard/Python/` | User |
| List Topics | GET | `/api/analytics/topics/` | User |
| Quiz History | GET | `/api/analytics/history/` | User |

---

## Testing Multiple Users

To properly test leaderboards:

1. Register another user: `jane_doe`
2. Login as `jane_doe` (get new token)
3. Take quizzes
4. Check leaderboard to see rankings change!

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Password auth failed" | Docker not running. Run: `docker-compose up -d` |
| "401 Unauthorized" | Token expired. Login again to get new token |
| "403 Forbidden" | You need admin token for that endpoint |
| "404 Not Found" | Check URL has trailing slash `/` |
| "Quiz creation failed" | Add Gemini API key to `.env` |

---

## 🎉 Congratulations!

You've tested a complete **LeetCode-style Quiz API** with:
- ✅ Admin creates quizzes on topics
- ✅ Users take quizzes
- ✅ Topic-based ELO rankings
- ✅ Global and topic leaderboards
- ✅ JWT Authentication
- ✅ AI-powered quiz generation

Great job for a beginner! 🚀
