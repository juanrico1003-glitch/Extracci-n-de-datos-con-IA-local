import fitz
import ollama
import pandas as pd
import json
import shutil
import os
import time

# Configuración de carpetas
INPUT_FOLDER = "facturas"
OUTPUT_FOLDER = "resultados"
LISTOS_FOLDER = "listos"
ERRORES_FOLDER = "errores"

for f in [OUTPUT_FOLDER, LISTOS_FOLDER, ERRORES_FOLDER]:
    os.makedirs(f, exist_ok=True)

def procesar_con_ia(texto_bloques):
    # Unimos bloques de texto asegurando que la IA lea el documento de forma lineal
    texto_plano = "\n".join([b[4] for b in texto_bloques])
    
    prompt = f"""
    Eres un experto en contabilidad. Tu tarea es extraer TODOS los productos de esta factura sin omitir ninguno.
    
    Reglas estrictas de extracción:
    1. CLIENTE: Busca 'Señores', extrae la empresa y la persona debajo.
    2. FECHA Y DIRECCIÓN: Identifica la línea que empieza por 'Mosquera' y termina en 2026.
    3. PRODUCTOS (TABLA): 
       - Identifica nombre usando 'Modelo' o 'Referencia'.
       - Identifica cantidad usando 'Cantidad' o 'Cant'.
       - Identifica valor unidad usando 'Valor unidad' o 'Valor unitario'.
       - DESCRIPCIÓN: Si dice 'Descripción' en la tabla, úsala. Si NO, busca bloques fuera de la tabla llamados 'Características' asociados al producto.
    
    4. IMPORTANTE: Extrae cada producto como una fila individual. Si hay 15 productos, el JSON debe tener 15 elementos en la lista 'productos'.
    
    Devuelve ÚNICAMENTE un JSON con este formato:
    {{
        "cliente": "nombre empresa + persona",
        "direccion_fecha": "la linea completa",
        "productos": [ {{"nombre": "...", "descripcion": "...", "cantidad": 0, "valor_unitario": 0}} ]
    }}
    Factura: {texto_plano}
    """
    
    response = ollama.chat(model='qwen2.5:7b', messages=[{'role': 'user', 'content': prompt}])
    content = response['message']['content'].strip().replace('```json', '').replace('```', '')
    
    try:
        return json.loads(content)
    except:
        start = content.find('{')
        end = content.rfind('}') + 1
        return json.loads(content[start:end])

data_final = []

for archivo in os.listdir(INPUT_FOLDER):
    if archivo.lower().endswith(".pdf"):
        ruta_origen = os.path.join(INPUT_FOLDER, archivo)
        print(f"Procesando: {archivo}...")
        
        try:
            doc = fitz.open(ruta_origen)
            bloques = []
            for pagina in doc:
                # Extraemos bloques en orden para mantener la lógica visual
                bloques.extend(pagina.get_text("blocks"))
            doc.close()
            
            datos = procesar_con_ia(bloques)
            
            for item in datos.get('productos', []):
                data_final.append({
                    "Nombre PDF": archivo,
                    "Direccion/Fecha": datos.get('direccion_fecha', 'N/A'),
                    "Producto": item.get('nombre', 'N/A'),
                    "Descripcion": item.get('descripcion', 'N/A'),
                    "Cantidad": item.get('cantidad', 0),
                    "valor unidad": item.get('valor_unitario', 0),
                    "Cliente": datos.get('cliente', 'N/A')
                })
            
            time.sleep(1)
            shutil.move(ruta_origen, os.path.join(LISTOS_FOLDER, archivo))
            
        except Exception as e:
            print(f"   X Error en {archivo}: {e}")
            time.sleep(1)
            try:
                shutil.move(ruta_origen, os.path.join(ERRORES_FOLDER, archivo))
            except:
                pass

if data_final:
    pd.DataFrame(data_final).to_excel(os.path.join(OUTPUT_FOLDER, "Base_Datos_Facturas.xlsx"), index=False)
    print("\n¡Proceso finalizado! Excel guardado.")