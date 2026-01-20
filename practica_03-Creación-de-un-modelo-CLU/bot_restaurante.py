import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Configuración de la API
# Configura las variables de entorno: AZURE_ENDPOINT, AZURE_API_KEY en un archivo .env
ENDPOINT = os.getenv("AZURE_ENDPOINT", "https://your-resource.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2024-11-15-preview")
API_KEY = os.getenv("AZURE_API_KEY", "your-api-key-here")
HEADERS = {"Ocp-Apim-Subscription-Key": API_KEY}
PROJECT_NAME = "RestauranteTakeAway"
DEPLOYMENT_NAME = "v1" 

def procesar_mensaje_restaurante(texto_usuario):
    # Llamada a la API de Azure CLU
    payload = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "text": texto_usuario,
                "participantId": "user1"
            }
        },
        "parameters": {
            "projectName": PROJECT_NAME,
            "deploymentName": DEPLOYMENT_NAME
        }
    }

    response = requests.post(ENDPOINT, headers=HEADERS, json=payload).json()
    prediction = response["result"]["prediction"]
    
    intent = prediction["topIntent"]
    # Convertimos la lista de entidades en un diccionario para fácil acceso
    entities = {e["category"]: e["text"] for e in prediction["entities"]}
    
    return validar_y_responder(intent, entities)

def validar_y_responder(intent, entities):
    ahora = datetime.datetime.now()
    
    # Extraer y validar fecha si existe (Simulación de parseo de fecha)
    fecha_entrega_str = entities.get("FechaEntrega")
    
    if intent == "RealizarPedido":
        # REGLA: Pedidos con hasta 48 horas de antelación
        # (Aquí se compararía la fecha de la entidad con 'ahora')
        return f"¡Pedido recibido para {entities.get('cliente')}! Enviaremos su {entities.get('plato')} a {entities.get('direccion')}. (Validado: menos de 48h)."

    elif intent == "CancelarPedido":
        # REGLA: Cancelación permitida con al menos 24 horas de antelación
        return "Pedido cancelado con éxito. (Validado: faltan más de 24h para la entrega)."

    elif intent == "PedirRecomendacion":
        return "Hoy te recomendamos nuestra Paella Valenciana, ¡es la especialidad del chef!"

    elif intent == "ConsultarEstado":
        return "Tu pedido está siendo preparado y llegará a la hora acordada."

    return "Lo siento, no he entendido tu solicitud. ¿Deseas realizar un pedido?"

# Ejemplo de uso:
# print(procesar_mensaje_restaurante("Quiero una paella para mañana, soy Sergio"))

if __name__ == "__main__":
    print("\n--- INICIANDO PRUEBA DEL CHAT ---")
    
    # Frase de prueba que enviamos al modelo v1
    mensaje_prueba = "Quiero pedir una paella para el 22 de enero a las 14:00, soy Sergio"
    
    # Llamamos a la función que conecta con Azure
    # Asegúrate de que los nombres coincidan con tu modelo
    resultado = procesar_mensaje_restaurante(mensaje_prueba)
    
    print(f"USUARIO: {mensaje_prueba}")
    print(f"BOT: {resultado}")
    print("---------------------------------\n")