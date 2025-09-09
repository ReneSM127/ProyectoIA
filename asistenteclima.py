import speech_recognition as sr
import requests
import os
import tempfile
import time
from gtts import gTTS
import pygame

class AsistenteClima:
    def __init__(self):
        
        # Cargar API key
        self.API_KEY = '9bcad0cadddfe10ca4f2ebd6112d3922'
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
        
        # Configurar reconocimiento de voz
        self.recognizer = sr.Recognizer()
        
        # Configurar micrófono
        try:
            self.microphone = sr.Microphone(device_index=0)
        except:
            self.microphone = sr.Microphone()
        
        # Configurar pygame para audio
        pygame.mixer.init()
        
        # Ajustar para ruido ambiental
        print("Ajustando para ruido ambiental...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("¡Asistente listo!")

    def hablar(self, texto):
        print(f"Asistente: {texto}")
        
        tmp_file_name = None
        try:
            tts = gTTS(text=texto, lang='es', slow=False)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_file_name = tmp_file.name
            
            tts.save(tmp_file_name)
            
            pygame.mixer.music.load(tmp_file_name)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.unload()
                
        except Exception as e:
            print(f"Error en síntesis de voz: {e}")
            print("(Modo texto por fallo de audio)")
            
        finally:
            if tmp_file_name and os.path.exists(tmp_file_name):
                try:
                    os.unlink(tmp_file_name)
                except Exception as e:
                    print(f"No se pudo eliminar el archivo temporal: {e}")

    def escuchar(self):
        
        print("Escuchando...")
        
        with self.microphone as source:
            try:
                # Escuchar con timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=4)
                print("Procesando audio...")
                
                # Reconocer usando Google
                texto = self.recognizer.recognize_google(audio, language='es-ES')
                print(f"Tú: {texto}")
                return texto.lower()
                
            except sr.WaitTimeoutError:
                print("Tiempo de espera agotado")
                return None
            except sr.UnknownValueError:
                print("No se pudo entender el audio")
                return None
            except sr.RequestError as e:
                print(f"Error con el servicio de voz: {e}")
                return None
            except Exception as e:
                print(f"Error inesperado al escuchar: {e}")
                return None
            
    def obtener_clima(self, ciudad):
        
        #Obtener datos del clima desde OpenWeatherMap
        if not self.API_KEY:
            self.hablar("Necesitas configurar la API key primero.")
            return None
        
        params = {
            'q': ciudad,
            'appid': self.API_KEY,
            'units': 'metric',
            'lang': 'es'
        }
        
        try:
            print(f"Consultando clima para: {ciudad}")
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f"Error API: Código {response.status_code}")
                return None
                
            datos = response.json()
            
            if datos.get('cod') != 200:
                print(f"Error API: {datos.get('message', 'Error desconocido')}")
                return None
            
            return datos
            
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None
    
    
    def formatear_respuesta(self, datos_clima):
        if not datos_clima:
            return "No obtuve información del clima."
        
        ciudad = datos_clima['name']
        temp_actual = round(datos_clima['main']['temp'])
        temp_min = round(datos_clima['main']['temp_min'])
        temp_max = round(datos_clima['main']['temp_max'])
        humedad = datos_clima['main']['humidity']
        descripcion = datos_clima['weather'][0]['description']
        
        mensaje = (
            f"En {ciudad}, la temperatura actual es de {temp_actual} grados. "
            f"Mínima de {temp_min} y máxima de {temp_max} grados. "
            f"Humedad del {humedad} por ciento. "
            f"Condiciones: {descripcion}."
        )
        
        return mensaje
    
    def ejecutar(self):
        #Bucle principal
        if not self.API_KEY:
            self.hablar("No tengo configurada la API key del clima")
            return
        
        self.hablar("¡Hola! Soy tu asistente del clima.")
        
        while True:
            self.hablar("¿De qué ciudad quieres saber el clima?")
            time.sleep(1)
            
            comando = self.escuchar()
            
            if not comando:
                self.hablar("No te escuché bien. ¿Podrías repetir?")
                continue
                        
            
            self.hablar(f"Buscando el clima para {comando.capitalize()}")
            datos_clima = self.obtener_clima(comando)
            
            if datos_clima:
                respuesta = self.formatear_respuesta(datos_clima)
                self.hablar(respuesta)
            else:
                self.hablar(f"Lo siento, no pude obtener el clima para {comando}")
            
            time.sleep(1)
            self.hablar("¿Quieres consultar otra ciudad? O puedes decirme adiós para finalizar")
            
            respuesta = self.escuchar()
            if any(palabra in respuesta for palabra in ['salir', 'terminar', 'adiós', 'chao']):
                self.hablar("¡Hasta luego! Que tengas un buen día.")
                break
            
            elif any(palabra in respuesta for palabra in ['Si', 'Sí', 'Continua']):
                continue

def main():
    """Función principal"""
    print("=" * 50)
    print("ASISTENTE DE VOZ PARA EL CLIMA")
    print("=" * 50)
    
    try:
        asistente = AsistenteClima()
        asistente.ejecutar()
        
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        try:
            pygame.mixer.quit()
        except:
            pass
        print("Programa terminado")

if __name__ == "__main__":
    main()