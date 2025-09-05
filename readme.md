# Asistente de Clima
Proyecto de IA

# Funcionamiento del código

## Librerías a utilizar
- SpeechRecognition <-- Utilizada para reconocer palabras de un audio
- pyaudio <-- Librería necesaria para instalar SpeechRecognition
- requests <-- Librería para hacer peticiones HTTP
- gTTS <-- Google Text to Speach, librería para pasar texto a voz
- pygame <-- Librería para crear videojuegos en python, sin embargo se utiliza por su capacidad de reproducir audio
- os <-- Librería para usar funciones del sistema operativo
- tempfile <-- Librería para crear archivos temporales

### Clase AsistenteClima
Primero se inicializa el Asistente con la API KEY de OpenWeatherMap y el end point
Además se configura el microfono de manera automática

#### Hablar()
Función dedicada para ingresar una cadena de texto y su salida será un audio que se reproduce.
Para ello se incializa el gTTS, luego se crea un archivo temporal en .mp3 y finalmente con pygame lo reproducimos

### Escuchar()
Función dedicada para pasar audio a una cadena de texto.

### obtener_clima()
Función dedicada a llamar a la API. 
```
params = {
    'q': ciudad,
    'appid': self.API_KEY,
    'units': 'metric',
    'lang': 'es'
}
```
- q: ciudad a consultar.
- appid: tu clave personal.
- units='metric': devuelve temperaturas en °C.
- lang='es': descripción del clima en español.
Cuando consultas a la API de OpenWeatherMap con el endpoint de clima actual (/data/2.5/weather), te devuelve un JSON parecido a este:
```
{
  "coord": {
    "lon": -86.8466,
    "lat": 21.1743
  },
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "cielo despejado",
      "icon": "01d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 30.45,
    "feels_like": 34.2,
    "temp_min": 29.0,
    "temp_max": 32.0,
    "pressure": 1012,
    "humidity": 65
  },
  "visibility": 10000,
  "wind": {
    "speed": 3.6,
    "deg": 90
  },
  "clouds": {
    "all": 0
  },
  "dt": 1693495023,
  "sys": {
    "type": 1,
    "id": 7118,
    "country": "MX",
    "sunrise": 1693470021,
    "sunset": 1693516421
  },
  "timezone": -18000,
  "id": 3531673,
  "name": "Cancún",
  "cod": 200
}

```
### formatear_respuesta()
Guarda la información relevante en un mensaje

### Ejecutar()
Bucle principal
