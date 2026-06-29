# Sistema de Extracción de Datos de Facturas (Document AI)

Este proyecto automatiza la extracción de datos desde facturas en formato PDF hacia un archivo Excel consolidado, utilizando Inteligencia Artificial local para interpretar formatos variables.

## Requisitos Previos

- **Python 3.12.10** instalado.
- **Ollama** instalado y corriendo localmente.

## Configuración Inicial

1. **Instalar el modelo de IA:**
   Abre tu terminal y ejecuta el siguiente comando para descargar el modelo necesario:

   ```bash
   ollama pull qwen2.5:7b

   ```

2. **Instalar dependencias:**
   Ejecuta el siguiente comando para instalar las librerías requeridas:

   ```bash
   pip install pandas openpyxl pymupdf ollama
   ```

3. **Crear las carpetas:**
   facturas, errores, listos y resultados en la base del proyecto
