from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "b3db802135669870652d71ab761cccbb"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

weather_translations = {
    'Clear': 'Despejado',
    'Clouds': 'Nublado',
    'Rain': 'Lluvia',
    'Drizzle': 'Llovizna',
    'Thunderstorm': 'Tormenta',
    'Snow': 'Nieve',
    'Mist': 'Neblina',
    'Smoke': 'Humo',
    'Haze': 'Bruma',
    'Dust': 'Polvo',
    'Fog': 'Niebla',
    'Sand': 'Arena',
    'Ash': 'Ceniza',
    'Squall': 'Chubasco',
    'Tornado': 'Tornado'
}

@app.route('/')
def index():
    return render_template('weather.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city'].strip()
    country = request.form['country'].strip()
    
    if not city or not country:
        return jsonify({'error': 'Por favor, ingrese una ciudad y un país válidos'}), 400
    
    url = f"{BASE_URL}?q={city},{country}&appid={API_KEY}&units=metric&lang=es"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado no exitosos
        
        data = response.json()

        # Verificación básica de contenido
        if 'weather' not in data or 'main' not in data:
            return jsonify({'error': 'Ciudad o país no encontrado o no válido'}), 404

        main_weather = data['weather'][0]['main']
        description = data['weather'][0]['description']
        
        translated_main = weather_translations.get(main_weather, main_weather)
        
        weather = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'description': f"{translated_main} ({description.capitalize()})",
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return jsonify(weather)
    
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return jsonify({'error': 'Ciudad o país no encontrado'}), 404
        else:
            return jsonify({'error': f'Error en la solicitud: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'Ocurrió un error: {err}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
