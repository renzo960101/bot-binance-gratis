import time
import requests
import telebot

# ========================================================
# ⚙️ CONFIGURACIÓN DE TUS CREDENCIALES (Poné las tuyas acá)
# ========================================================
TOKEN = "8885744579:AAH-XmdXemge0sNbSUmKFCneRFBXByaREYY"
CHAT_ID = "8885746151"

# Inicializamos el bot de Telegram
bot = telebot.TeleBot(TOKEN)

# URL pública de la API de Binance para cotizaciones
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# Variables para controlar el estado del bot
ULTIMO_PRECIO = 0.0

def obtener_precio_bitcoin():
    """Función para conectarse a Binance y traer el precio actual de BTC."""
    try:
        respuesta = requests.get(BINANCE_API_URL, timeout=10)
        datos = respuesta.json()
        return float(datos['price'])
    except Exception as e:
        print(f"Error al conectar con Binance: {e}")
        return None

def iniciar_bot():
    """Bucle principal que corre en la nube vigilando el precio."""
    global ULTIMO_PRECIO
    
    print("🤖 El bot de Binance arrancó con éxito en la nube de GitHub...")
    
    # Mensaje de bienvenida para avisarte que ya está online
    try:
        bot.send_message(CHAT_ID, "🚀 ¡Hola Renzx! El bot ya está activo en la nube y vigilando Binance 24/7.")
    except Exception as e:
        print(f"Error al enviar mensaje de bienvenida: {e}. Revisá el Token o Chat ID.")

    # Acortamos el bucle para que se ejecute rápido dentro de la ventana de GitHub Actions
    # Corre durante un par de minutos controlando el precio cada 8 segundos
    for _ in range(15):
        precio_actual = obtener_precio_bitcoin()
        
        if precio_actual:
            print(f"Precio actual: ${precio_actual:,} USDT")
            
            # Si es la primera vuelta, guardamos el precio inicial
            if ULTIMO_PRECIO == 0.0:
                ULTIMO_PRECIO = precio_actual
            
            # Ejemplo: Si el precio cambia más de $50 USDT, te avisa al celu
            diferencia = abs(precio_actual - ULTIMO_PRECIO)
            if diferencia >= 50.0:
                mensaje = f"⚠️ ¡Movimiento en Binance!\n\n📈 El Bitcoin cambió ${diferencia:.2f} USDT.\n💰 Precio actual: ${precio_actual:,} USDT"
                try:
                    bot.send_message(CHAT_ID, mensaje)
                    ULTIMO_PRECIO = precio_actual  # Actualizamos el último precio avisado
                except Exception as e:
                    print(f"Error al enviar alerta de Telegram: {e}")
        
        # Espera 8 segundos antes de volver a mirar Binance
        time.sleep(8)

if __name__ == "__main__":
    iniciar_bot()
