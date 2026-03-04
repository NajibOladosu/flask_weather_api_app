from datetime import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

API_KEY = '6bbea12952412fe6c1bbb88ffb069f31'
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'temperature': self.temperature,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }
    
    def get_weather_from_api(city):
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        # try:
        response = requests.get(WEATHER_API_URL, params=params)
        # except requests.RequestException as e:
        #     print(f"Error fetching weather data: {e}")
        #     return None

        if response.status_code == 200:
            data = response.json()
            return {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description']
            }
        else:
            return response.json()
        
@app.route('/weather')
def get_weather():
    city = request.args.get('q')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    weather_data = Weather.get_weather_from_api(city)
    if weather_data:
        weather = Weather(
            city=weather_data['city'],
            temperature=weather_data['temperature'],
            description=weather_data['description'],
            timestamp=datetime.utcnow()
        )
        db.session.add(weather)
        db.session.commit()
        return jsonify(weather.to_dict())
    else:
        return jsonify({'error': 'Could not fetch weather data'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)