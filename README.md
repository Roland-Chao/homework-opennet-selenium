# OpenNet Homework - Test Automation Framework

Pytest + Selenium + Requests test automation framework

## Project Structure

```
homework-opennet-selenium/
│
├── api_object/                     # API object layer
│   ├── __init__.py
│   ├── httpbin_org.py             # HTTPBin API wrapper
│   └── the_dog_api.py             # The Dog API wrapper
│
├── config/                         # Configuration files
│   ├── __init__.py
│   └── browser_config.py          # Browser configuration
│
├── library/                        # Shared utilities
│   ├── __init__.py
│   ├── allure.py                  # Allure report utilities
│   ├── api_utils.py               # API testing utilities
│   ├── element.py                 # Element wrapper
│   ├── exception.py               # Exception handling
│   ├── file_handler.py            # File handling utilities
│   ├── logger.py                  # Logging utilities
│   ├── page_utils.py              # Page operation utilities
│   └── validator.py               # Data validation utilities
│
├── page_objects/                   # Page object layer
│   ├── __init__.py
│   └── twitch/
│       ├── __init__.py
│       ├── home_page/
│       │   ├── __init__.py
│       │   ├── locator.py
│       │   └── action.py
│       └── search_page/
│           ├── __init__.py
│           ├── locator.py
│           └── action.py
│
├── test_api/                       # API test cases
│   ├── __init__.py
│   ├── httpbin/
│   │   ├── __init__.py
│   │   ├── test_httpbin_org_post.py
│   │   └── case_data/
│   │       ├── verify_error.json
│   │       └── verify_success.json
│   └── the_dog_api/
│       ├── __init__.py
│       ├── test_dog_api_favourites.py
│       └── case_data/
│           ├── favourite_success.json
│           └── favourite_error.json
│
├── test_twitch/                    # Twitch UI test cases
│   ├── __init__.py
│   ├── test_twitch_stream_search.py
│   └── case_data/
│       └── twitch_search.json
│
├── conftest.py                     # Pytest configuration and fixtures
├── pytest.ini                      # Pytest settings
├── requirements.txt                # Python dependencies
├── setup_and_test.sh              # Setup and test execution script
├── .env                            # Environment variables (API Keys)
└── .gitignore                      # Git ignore file
```

## Quick Start

### Run Setup and Test Script

```bash
chmod +x setup_and_test.sh
./setup_and_test.sh
```

This script will:
- Create Python virtual environment
- Install all dependencies
- Verify imports
- Run all tests
- Generate Allure reports

## Manual Test Execution

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest -m "UI or API" -v

# Run API tests only
pytest -m API -v

# Run UI tests only
pytest -m UI -v

# View Allure report
allure serve allure-results
```