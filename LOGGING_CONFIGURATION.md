# Logging Configuration

## Overview

The Mimir project uses Django's logging framework with separate log files for application and test logs.

---

## Application Logging

### Configuration

**Location**: `mimir/settings.py` - `LOGGING` dictionary

**Log File**: `app.log` (in project root)

**Log Level**: `INFO` (default)

**Rotation**: None - log file is **overwritten on each restart** (`mode='w'`)

### Format

```
{levelname} {asctime} {module} {funcName} {lineno} {message}
```

**Example Output**:
```
INFO 2025-11-15 23:39:17,782 create_default_admin handle 26 User "admin" already exists
INFO 2025-11-15 23:40:23,456 views form_valid 21 Login attempt for user: admin, remember_me: False
INFO 2025-11-15 23:40:23,458 views form_valid 30 User admin logged in without remember me (2 weeks)
INFO 2025-11-15 23:41:15,789 views custom_logout_view 41 User admin logged out successfully
```

### Handlers

1. **File Handler** (`app.log`)
   - Level: INFO
   - Mode: 'w' (overwrite on restart)
   - Format: Verbose (includes module, function, line number)

2. **Console Handler** (stdout)
   - Level: INFO
   - Format: Simple (level + message)
   - Provides immediate feedback during development

### Loggers

**Root Logger**:
- Handlers: file + console
- Level: INFO
- Catches all logging from application

**Django Logger**:
- Handlers: file + console
- Level: INFO
- Django framework logs
- Does not propagate to root

**Accounts Logger**:
- Handlers: file + console
- Level: INFO
- Authentication-related logs
- Does not propagate to root

**Methodology Logger**:
- Handlers: file + console
- Level: INFO
- Methodology app logs
- Does not propagate to root

---

## Test Logging

### Configuration

**Location**: `pytest.ini`

**Log File**: `tests.log` (in project root)

**Log Level**: `DEBUG` (captures everything)

### Format

```
%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s
```

**Example Output**:
```
DEBUG 2025-11-15 18:39:17 test_auth_config test_login_url_configured 10 Testing LOGIN_URL configuration
INFO 2025-11-15 18:39:17 test_auth_config test_login_url_configured 11 LOGIN_URL is correctly set
```

### Configuration Options

**pytest.ini settings**:
```ini
log_file = tests.log
log_file_level = DEBUG
log_file_format = %%(levelname)s %%(asctime)s %%(module)s %%(funcName)s %%(lineno)d %%(message)s
log_file_date_format = %%Y-%%m-%%d %%H:%%M:%%S
```

**Note**: Double `%%` is required in pytest.ini to escape the percent signs.

---

## Usage

### Application Logs

**Start Django server**:
```bash
python manage.py runserver
# Logs written to app.log + console output
```

**Run management command**:
```bash
python manage.py create_default_admin
# Logs written to app.log + console output
```

**View logs**:
```bash
# View entire log
cat app.log

# Tail log (follow in real-time)
tail -f app.log

# Search for specific user
grep "admin" app.log

# Filter by level
grep "ERROR" app.log
```

### Test Logs

**Run tests**:
```bash
pytest tests/
# Test output written to tests.log
```

**Run specific test with logging**:
```bash
pytest tests/unit/test_auth_config.py -v
# Output to tests.log + console
```

**View test logs**:
```bash
# View entire test log
cat tests.log

# View last test run
tail -50 tests.log
```

---

## Log Files Location

```
/Users/denispetelin/GitHub/mimir/
├── app.log          # Application logs (overwritten on restart)
├── tests.log        # Test logs (overwritten on test run)
├── mimir/
│   └── settings.py  # Logging configuration
└── pytest.ini       # Test logging configuration
```

---

## Git Ignore

Both log files are added to `.gitignore`:
```gitignore
# Application logs
app.log
tests.log
```

**Rationale**: Log files are runtime artifacts and should not be committed to version control.

---

## Logging Best Practices

### When to Log

**INFO Level**:
- User login/logout events
- Important state changes
- Successful operations
- Management command execution

**WARNING Level**:
- Unexpected conditions that don't prevent operation
- Deprecated feature usage
- Authentication attempts by unauthenticated users

**ERROR Level**:
- Exception handling
- Failed operations
- Database errors
- Configuration problems

**DEBUG Level** (not written to app.log by default):
- Detailed diagnostic information
- Variable values
- Flow tracing
- Use in development/testing only

### What to Log

**Always Include**:
- Username (for user actions)
- Operation being performed
- Result (success/failure)
- Key identifiers (IDs, names)

**Never Include**:
- Passwords
- Session tokens
- API keys
- Sensitive personal data

### Example Logging

**Good**:
```python
logger.info(f"User {username} logged in with remember me (30 days)")
logger.warning(f"Logout attempted by unauthenticated user")
logger.error(f"Error creating superuser: {e}")
```

**Bad**:
```python
logger.info(f"User {username} logged in with password {password}")  # ❌ Never log passwords
logger.info("Login happened")  # ❌ Too vague
logger.error("Error")  # ❌ No context
```

---

## Troubleshooting

### Log File Not Created

**Issue**: `app.log` doesn't exist after starting server

**Solution**:
1. Check `BASE_DIR` in settings.py
2. Verify logging configuration is present
3. Ensure logger is imported: `logger = logging.getLogger(__name__)`
4. Check file permissions in project directory

### No Test Output in tests.log

**Issue**: `tests.log` is empty after running tests

**Cause**: Unit tests may not produce log output if they only test configuration

**Solution**: Run tests that execute code with logging:
```bash
pytest tests/e2e/ -v  # E2E tests will produce more logs
```

### Log File Growing Too Large

**Issue**: `app.log` becomes very large

**Solution**: The log file is automatically cleared on each restart (`mode='w'`). No rotation needed.

If you need rotation, change in settings.py:
```python
'file': {
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': BASE_DIR / 'app.log',
    'maxBytes': 10485760,  # 10MB
    'backupCount': 5,
    'mode': 'a',  # Append instead of overwrite
    'formatter': 'verbose',
},
```

### Logging Not Working in Tests

**Issue**: Logger calls don't appear in tests.log

**Cause**: Logger not configured in test

**Solution**: Use pytest's caplog fixture:
```python
def test_something(caplog):
    with caplog.at_level(logging.INFO):
        # Your code that logs
        assert "Expected message" in caplog.text
```

---

## Production Recommendations

### For Production Deployment:

1. **Use a log aggregation service** (e.g., CloudWatch, Datadog, Sentry)

2. **Enable log rotation**:
   ```python
   'class': 'logging.handlers.TimedRotatingFileHandler',
   'when': 'midnight',
   'backupCount': 30,
   ```

3. **Increase log level to WARNING** (reduce noise):
   ```python
   'root': {
       'level': 'WARNING',
   }
   ```

4. **Use JSON formatting** (easier to parse):
   ```python
   'format': '{"time":"%(asctime)s","level":"%(levelname)s","module":"%(module)s","message":"%(message)s"}',
   ```

5. **Add request ID tracking** (for distributed tracing)

6. **Set up alerts** for ERROR level logs

7. **Monitor log volume** and adjust levels accordingly

---

## Configuration Summary

| Aspect | Application (app.log) | Tests (tests.log) |
|--------|----------------------|-------------------|
| **Location** | Project root | Project root |
| **Level** | INFO | DEBUG |
| **Format** | Verbose | Verbose |
| **Rotation** | None (overwrite) | None (overwrite) |
| **Handlers** | File + Console | File only |
| **Committed** | No (gitignored) | No (gitignored) |

---

## Verification

**Test application logging**:
```bash
python manage.py create_default_admin
cat app.log
# Should see: INFO ... create_default_admin handle 26 User "admin" already exists
```

**Test test logging**:
```bash
pytest tests/unit/test_auth_config.py -v
cat tests.log
# Should contain test execution logs (may be empty for config tests)
```

**Both working**: ✅

---

**Last Updated**: November 15, 2025  
**Configuration Version**: 1.0  
**Status**: Production-ready ✅
