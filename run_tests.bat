@echo off
REM ================================================
REM Quiz API Automated Test Runner
REM ================================================

echo ================================================
echo   Quiz API - Automated Testing
echo ================================================
echo.

REM Check if Newman is installed
where newman >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Newman is not installed!
    echo.
    echo To install Newman, run:
    echo   npm install -g newman
    echo.
    echo Or install Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Create test reports directory if not exists
if not exist "test-reports" mkdir test-reports

echo [1/3] Starting Django server...
start /B python manage.py runserver > server.log 2>&1

REM Wait for server to start
echo [2/3] Waiting for server to be ready...
timeout /t 5 /nobreak > nul

REM Check if server is running
curl -s http://127.0.0.1:8000/api/ >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Server is not responding!
    echo Please check if port 8000 is available.
    echo.
    pause
    exit /b 1
)

echo [3/3] Running automated tests with Newman...
echo.
echo ================================================
echo.

REM Run Newman with the collection
newman run postman_collection.json ^
    -e postman_environment.json ^
    --export-environment test-reports/postman_environment.json ^
    --delay-request 500 ^
    --timeout-request 10000 ^
    --reporters cli,json,html ^
    --reporter-json-export test-reports/report.json ^
    --reporter-html-export test-reports/report.html

REM Store exit code
set TEST_EXIT_CODE=%ERRORLEVEL%

echo.
echo ================================================
echo Test Results Summary
echo ================================================
echo.
echo Reports saved to:
echo   - test-reports/report.json
echo   - test-reports/report.html
echo.

REM Stop the server
taskkill /F /IM python.exe >nul 2>&1

if %TEST_EXIT_CODE% EQU 0 (
    echo SUCCESS: All tests passed!
) else (
    echo FAILURE: Some tests failed!
)

echo.
pause
exit /b %TEST_EXIT_CODE%
