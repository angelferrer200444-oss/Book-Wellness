import requests
import time

def obtener_json(url, intentos=5):

    for i in range(intentos):

        try:

            respuesta = requests.get(
                url,
                timeout=(10, 20)
            )

            respuesta.raise_for_status()

            return respuesta.json()

        except requests.exceptions.RequestException as e:

            print(f"Intento {i + 1} falló")
            print("URL:", url)
            print("ERROR:", e)

            if i < intentos - 1:
                time.sleep(1)

    print("Se agotaron los intentos")

    return None
