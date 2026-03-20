# Automated Testing Setup

> **What I built:** Postman + Newman testing infrastructure for comprehensive API testing

## Files

| File | Purpose |
|------|---------|
| postman_collection.json | 20+ automated test requests |
| postman_environment.json | Environment config |
| test_data.json | 30 data-driven test cases |
| run_tests.bat | One-click Windows test runner |

## Test Coverage (34 cases)

- **Auth (5):** Registration, login, validation, errors
- **Quizzes (4):** Create, list, questions, delete
- **Attempts (4):** Start, answer, submit, validation
- **Analytics (5):** Stats, leaderboards, history, topics
- **Security (3):** No token, invalid token, forbidden
- **Edge Cases (5):** Non-existent IDs, empty fields

## Running Tests

**Postman GUI:**
1. Import collection + environment
2. Runner → Select collection → Run

**Command Line:**
```bash
newman run postman_collection.json -e postman_environment.json
```

**Windows:**
```bash
run_tests.bat
```

## How I Built It

Each request has test scripts that run automatically:
```javascript
pm.test('Quiz created', function() {
    pm.expect(pm.response.json()).to.have.property('id');
    pm.environment.set('quiz_id', pm.response.json().id);
});
```

## Key Features

- **Auto-variables** - IDs stored for chained requests
- **Token handling** - Automatic JWT management
- **Chained flow** - Register → Login → Create → Attempt → Submit
- **Performance checks** - <2s response time validation

## Test Flow

```
Register Admin → Login → Create Quiz → 
Register User → Login → List Quiz → 
Get Questions → Start Attempt → 
Submit Answer → Submit Quiz → 
Check Stats → View Leaderboard
```

## Troubleshooting

- Newman not found: `npm install -g newman`
- Port 8000 in use: Stop server or change port
- Tests fail: Check `docker-compose ps` and migrations

---

**Testing ensures the API works end-to-end, not just happy paths**
