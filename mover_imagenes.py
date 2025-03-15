import os
import shutil
from pathlib import Path

directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Rutas de origen y destino (usando rutas absolutas)
ruta_origen = os.path.join(directorio_actual, "images_pdf")
ruta_destino = os.path.join(directorio_actual, "imagenes_fichas")

# Información de depuración inicial
print(f"Directorio actual: {directorio_actual}")
print(f"Buscando imágenes en: {ruta_origen}")
print(f"Copiando a: {ruta_destino}")

# Verificar que la carpeta origen existe
if not os.path.exists(ruta_origen):
    print(f"Error: La carpeta '{ruta_origen}' no existe.")
    exit(1)

# Crear la carpeta de destino (asegurarse de que se crea)
try:
    print(f"Intentando crear la carpeta destino: {ruta_destino}")
    os.makedirs(ruta_destino, exist_ok=True)
    print(f"Carpeta destino creada o ya existente: {ruta_destino}")
    
    # Verificar que se haya creado la carpeta
    if not os.path.exists(ruta_destino):
        print(f"Error: No se pudo crear la carpeta '{ruta_destino}'.")
        exit(1)
except Exception as e:
    print(f"Error al crear la carpeta de destino: {str(e)}")
    exit(1)

# Contador para los nuevos nombres de archivo
contador = 1

try:
    # Recorrer toda la estructura de directorios
    for raiz, directorios, archivos in os.walk(ruta_origen):
        # Verificar si estamos en una carpeta llamada 'pages'
        if os.path.basename(raiz) == 'pages':
            # Obtener el nombre de la carpeta padre (que contiene la carpeta 'pages')
            carpeta_padre = os.path.basename(os.path.dirname(raiz))
            print(f"Procesando carpeta: {carpeta_padre}")
            
            # Recorrer los archivos en este directorio
            for archivo in archivos:
                # Verificar si es un archivo PNG
                if archivo.lower().endswith('.png'):
                    try:
                        # Construir la ruta completa del archivo origen
                        ruta_archivo_origen = os.path.join(raiz, archivo)
                        
                        # Crear un nuevo nombre único basado en la carpeta padre y contador
                        # Eliminar caracteres problemáticos
                        carpeta_padre_seguro = "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in carpeta_padre)
                        nuevo_nombre = f"{carpeta_padre_seguro}_{contador}.png"
                        
                        # Construir la ruta completa de destino
                        ruta_archivo_destino = os.path.join(ruta_destino, nuevo_nombre)
                        
                        # Verificar que el archivo origen existe
                        if not os.path.exists(ruta_archivo_origen):
                            print(f"Advertencia: Archivo origen no encontrado: {ruta_archivo_origen}")
                            continue
                            
                        # Copiar el archivo
                        print(f"Copiando: {ruta_archivo_origen} -> {ruta_archivo_destino}")
                        shutil.copy2(ruta_archivo_origen, ruta_archivo_destino)
                        print(f"Copiado exitosamente: {nuevo_nombre}")
                        
                        # Incrementar el contador
                        contador += 1
                    except Exception as e:
                        print(f"Error al copiar {archivo}: {str(e)}")

    print(f"\nProceso completado. Se copiaron {contador-1} archivos a la carpeta '{ruta_destino}'.")

except Exception as e:
    print(f"Error durante la ejecución: {str(e)}")