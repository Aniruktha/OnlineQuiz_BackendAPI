# Postman Automated Testing Setup

This directory contains everything you need to run automated tests for the Quiz API.

> **Note**: The API now supports both `option_id` and `selected_option_id` for submitting answers.
> The test data includes 34 comprehensive test cases covering all endpoints.

## Files Overview

| File | Description |
|------|-------------|
| [`postman_collection.json`](postman_collection.json) | Postman collection with 20 automated test requests |
| [`postman_environment.json`](postman_environment.json) | Environment variables for testing |
| [`newman-config.json`](newman-config.json) | Newman CLI configuration |
| [`run_tests.bat`](run_tests.bat) | Windows batch script to run all tests |

---

## Quick Start

### Option 1: Run Tests in Postman (GUI)

1. Open **Postman**
2. Click **Import** button (top left)
3. Drag and drop [`postman_collection.json`](postman_collection.json)
4. Import [`postman_environment.json`](postman_environment.json) as environment
5. Select the imported environment from dropdown
6. Click **Runner** (top right)
7. Select "Quiz API - Automated Tests" collection
8. Click **Run**

### Option 2: Run Tests from Command Line (Newman)

1. Install Node.js from https://nodejs.org/
2. Install Newman:
   ```cmd
   npm install -g newman
   ```
3. Run tests:
   ```cmd
   cd quiz_api
   newman run postman_collection.json -e postman_environment.json
   ```

### Option 3: Run Automated Script

Simply double-click [`run_tests.bat`](run_tests.bat) - it will:
- Start the Django server
- Run all automated tests
- Generate HTML/JSON reports
- Stop the server

---

## Test Data File

The [`test_data.json`](test_data.json) file contains **30 test cases** covering:

| Test Category | Count | Examples |
|---------------|-------|----------|
| User Registration | 5 | Valid user, duplicate username, invalid email, short password |
| Authentication | 4 | Admin login, user login, wrong password, non-existent user |
| Quiz Creation | 4 | Python quiz, JavaScript quiz, invalid topic, unauthorized creation |
| Quiz Operations | 4 | List, questions, start attempt, submit |
| Analytics | 5 | Stats, topic stats, leaderboard, topics, history |
| Security | 3 | No token, invalid token, forbidden access |
| Edge Cases | 5 | Non-existent quiz, empty fields, filter history |

### Example Test Case Structure:
```json
{
    "test_name": "Admin User Registration",
    "username": "admin_user",
    "email": "admin@test.com",
    "password": "admin123",
    "is_admin": true,
    "expected_status": 200,
    "description": "Register an admin user"
}
```

---

## What's Being Tested

### Authentication Tests
- ✅ User registration
- ✅ Admin login
- ✅ User login
- ✅ Token validation
- ✅ Unauthorized access (401)
- ✅ Invalid token (403)

### Admin Features
- ✅ Create quiz (Python)
- ✅ Create quiz (JavaScript)

### User Features
- ✅ List all quizzes
- ✅ Get quiz questions
- ✅ Start quiz attempt
- ✅ Submit answer
- ✅ Submit quiz
- ✅ Get user stats
- ✅ Get topic stats
- ✅ View global leaderboard
- ✅ View topic leaderboard
- ✅ List topics
- ✅ View quiz history

### Performance Tests
- ✅ Response time checks
- ✅ Request timeout handling

---

## Test Scripts Included

Each request in the collection has **automatic test scripts** that verify:

```javascript
// Example test script
pm.test('Quiz created successfully', function() {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.environment.set('quiz_id', jsonData.id);
});

pm.test('Response time is acceptable', function() {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});
```

### Key Test Features

1. **Auto-variables**: Tests automatically store IDs for use in subsequent requests
2. **Token management**: Automatic token refresh handling
3. **Assertions**: Verify response structure, status codes, and data
4. **Performance**: Response time monitoring
5. **Chained requests**: Each test builds on previous results

---

---

## Data-Driven Testing

For more comprehensive testing, use the data-driven collection that iterates through test cases:

### Import Data-Driven Collection:
1. In Postman, click **Import**
2. Import [`postman_data_driven.json`](postman_data_driven.json)
3. Import [`test_data.json`](test_data.json) as your test data
4. In Runner, select "Quiz API - Data Driven Tests"
5. Check **Data** and select `test_data.json`
6. Check **Persistence** to save variables
7. Click **Run**

### Run with Newman (CLI):
```cmd
newman run postman_data_driven.json -d test_data.json -e postman_environment.json
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          npm install -g newman
      
      - name: Start services
        run: docker-compose up -d
      
      - name: Run Django migrations
        run: python manage.py migrate
      
      - name: Run Newman tests
        run: newman run postman_collection.json -e postman_environment.json
      
      - name: Upload test reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-reports
          path: test-reports/
```

---

## Viewing Test Reports

### HTML Report
Open `test-reports/report.html` in a browser for a visual report.

### JSON Report
Use `test-reports/report.json` for programmatic access:

```bash
# Get test summary
cat test-reports/report.json | jq '.run.stats'
```

---

## Troubleshooting

### Newman not found
```cmd
npm install -g newman
```

### Port 8000 in use
Stop any running servers or change port in [`postman_environment.json`](postman_environment.json)

### Tests failing
1. Ensure Docker is running: `docker-compose ps`
2. Ensure database is migrated: `python manage.py migrate`
3. Check server logs: `python manage.py runserver`

### Import errors in Postman
- Make sure you're importing the JSON files (not the folder)
- Check that JSON is valid using https://jsonlint.com/

---

## Adding More Tests

To add tests to a request in Postman:

1. Open the request
2. Go to **Tests** tab
3. Add your test script:
   ```javascript
   pm.test('Your test name', function() {
       // Your assertions
       pm.expect(pm.response.json()).to.have.property('expected_field');
   });
   ```

4. Export the collection again to update [`postman_collection.json`](postman_collection.json)

---

## Support

- Postman Docs: https://learning.postman.com/docs/
- Newman Docs: https://github.com/postmanlabs/newman
- This project's API: See [`TESTING_GUIDE.md`](TESTING_GUIDE.md)
