1. Build a Weather Data Service with Flask
Objective
Develop a Flask application to fetch weather data from an external API, store it in a database, and implement caching for optimization.
Task Details
Endpoint: Create a /weather?city=<city_name> endpoint.
Database:
Use SQLAlchemy with a table for Weather data (fields: city_name, temperature, description, timestamp).
External API Integration:
Fetch weather data using an external API (e.g., OpenWeatherMap).
Use the API key: 6bbea12952412fe6c1bbb88ffb069f31
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
Store the fetched data in the database.
Caching:
Cache data for 10 minutes using an in-memory store to reduce API calls.
Endpoint Behavior:
Return cached data if available.
Use the database if the cache is unavailable and the data is valid (<10 minutes old).
Fetch fresh data if neither cache nor valid database data exists.