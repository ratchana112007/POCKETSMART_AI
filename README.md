# PocketSmart_AI – Smart Budget & Recommendation Assistant

## Features

- Secure session-based registration/login
- SQLite + SQLAlchemy persistence
- Home interior planner
- Party/event planner
- Jewelry planner
- Google Gemini AI recommendations
- Rule-based fallback when Gemini is unavailable
- Recommendation history
- External search/platform links
- Responsive Jinja2 UI
- Automated API tests

## Project structure

```text
PocketSmart_AI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── dependencies.py
│   ├── ai/
│   │   ├── __init__.py
│   │   └── gemini_service.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── pages.py
│   │   ├── auth.py
│   │   └── recommendations.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── catalog.py
│   │   ├── platform_links.py
│   │   └── recommendation_service.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── home_planner.html
│   │   ├── party_planner.html
│   │   ├── jewelry_planner.html
│   │   ├── recommendations.html
│   │   └── history.html
│   └── static/
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── app.js
│       └── uploads/
│           └── .gitkeep
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md