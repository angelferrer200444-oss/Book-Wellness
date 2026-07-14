import requests
import time

def obtener_json(url, params=None, timeout=(10, 20), intentos=5):

    for i in range(intentos):

        try:

            print(f"Intento {i + 1}/{intentos} -> {url}")

            respuesta = requests.get(
                url,
                params=params,
                timeout=timeout
            )


            respuesta.raise_for_status()

            return respuesta.json()

        except requests.exceptions.RequestException as e:

            print(f"Intento {i + 1} falló")
            print("URL:", url)
            print("ERROR:", e)

            if i < intentos - 1:
                print("Reintentando en 1 segundo...\n")
                time.sleep(1)

    print(f"Se agotaron los {intentos} intentos.")

    return None
