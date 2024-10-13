# Movies Recommendation System

A FastAPI-based movie recommendation system under active development. The goal of this application is to provide movie recommendations using various algorithms, including popularity-based, collaborative filtering, and content-based approaches, each accessible through separate API endpoints.

## Main Features
- **Popularity-Based Recommendations:** Uses a weighted rating system to rank movies.
- **Content-Based Recommendations:** Provides movie suggestions based on movie metadata such as genres, cast, and crew.
- **Collaborative Recommendations:** Recommends movies based on user interactions and preferences.

## Endpoints
1. :white_check_mark: `/popularity` - Provides popularity-based movie recommendations.
2. :white_check_mark: `/content` - Content-based movie recommendations.
3. :white_check_mark: `/collaborative` - Collaborative-based recommendations.


## Current Status
- All 3 recommendation systems are currently being developed.
- ![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)
- CI Integration: GitHub Actions runs automated tests on every push to ensure code quality.

## Next Steps:
- Implement Dependency Injection: To improve flexibility, testability, and maintainability by decoupling components.
- Database Integration: Transition from loading data from CSV files to using a simple database (e.g., SQLite, PostgreSQL) for better scalability and data management.
- API Enhancements: Create additional endpoints to POST, PUT, and DELETE data, enabling dynamic data manipulation and management through the API.

