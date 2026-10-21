import os
from PIL import Image
import urllib.parse
import sys

# Configurar autocompletado de carpetas según el sistema operativo
try:
    import readline
except ImportError:
    try:
        # En Windows puede requerir: pip install pyreadline3
        import pyreadline3 as readline
    except ImportError:
        readline = None

def completar_rutas(text, state):
    text = os.path.expanduser(text)
    if os.path.isdir(text):
        dir_path = text
        prefix = ""
    else:
        dir_path, prefix = os.path.split(text)
        if not dir_path:
            dir_path = "."
    try:
        items = os.listdir(dir_path)
    except OSError:
        return None
    matches = [
        os.path.join(dir_path, item) if dir_path != "." else item
        for item in items if item.startswith(prefix)
    ]
    results = []
    for m in matches:
        if os.path.isdir(os.path.expanduser(m)):
            results.append(m + os.sep)
        else:
            results.append(m)
    try:
        return results[state]
    except IndexError:
        return None

if readline:
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completar_rutas)

# ==========================================
# INICIO DEL SCRIPT PRINCIPAL
# ==========================================

BASE_URL_GENERAL = "https://raw.githubusercontent.com/TheCONDIMENTSoficialxd/torizo-webpage-assets/main/galeria/"

print("--- Generador Automático de HTML para Galería ---")
print("Tip: Usa la tecla [TAB] para autocompletar rutas de carpetas.\n")

# 1. Pedir al usuario la ubicación de la carpeta principal "galeria"
folder = input("Introduce la ruta de la carpeta principal que contiene los subdirectorios (galeria): ").strip()
folder = os.path.expanduser(folder)
html_folder = input("Introduce la ruta de la carpeta donde se guardará el HTML: ").strip()
html_folder = os.path.expanduser(html_folder)

if not os.path.isdir(folder):
    print(f"\nError: la carpeta '{folder}' no existe o no es válida.")
    exit()


if not os.path.isdir(html_folder):
    print(f"\nError: la carpeta '{html_folder}' no existe o no es válida.")
    exit()

# 2. Configurar la relación entre los nombres de carpetas y los IDs/Tags
directorios_tags = {
    "conceptual": "tag1",
    "paisajes": "tag2",
    "autorretratos": "tag3",
    "posters": "tag4"
}

# 3. Ruta del archivo de salida
html_output_path = os.path.join(html_folder, "index.html")

print(f"\nEscaneando subdirectorios y generando '{html_output_path}'...")

# 4. Crear o sobreescribir el archivo index.html
with open(html_output_path, "w", encoding="utf-8") as html_file:
    # Recorrer cada directorio predefinido
    for nombre_dir, tag_id in directorios_tags.items():
        dir_path = os.path.join(folder, nombre_dir)
        
        # Verificar si la carpeta existe dentro de la ruta especificada
        if not os.path.isdir(dir_path):
            print(f"  [!] Advertencia: No se encontró la carpeta '{nombre_dir}'. Se omitirá.")
            continue
            
        print(f"  -> Procesando directorio: {nombre_dir} (se asignará {tag_id})")
        base_url_especifica = f"{BASE_URL_GENERAL}{nombre_dir}/"
        
        # Recorrer las imágenes dentro del subdirectorio
        for filename in os.listdir(dir_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                filepath = os.path.join(dir_path, filename)
                
                # Obtener el tamaño de la imagen
                try:
                    with Image.open(filepath) as img:
                        width, height = img.size
                except Exception as e:
                    print(f"      [x] Error al leer {filename}: {e}")
                    continue
                
                # Formatear variables para el HTML
                url = base_url_especifica + urllib.parse.quote(filename)
                title = os.path.splitext(filename)[0]
                html_id = title.replace(" ", "-").lower()
                
                # Bloque HTML para el elemento actual
                html = f'''<li class="grid-item entry {tag_id}" id="{html_id}">\n  <figure>\n    <a\n      href="{url}"\n      data-img="{url}"\n      data-thumb="{url}"\n      data-alt="{title}"\n      data-caption="{title}"\n      data-width="{width}"\n      data-height="{height}"\n    >\n      <img\n        loading="lazy"\n        class="responsive"\n        width="{width}"\n        height="{height}"\n        src="{url}"\n        alt="{title}"\n      />\n    </a>\n    <figcaption class="caption">{title}</figcaption>\n  </figure>\n</li>\n'''
                
                # Escribir en el archivo
                html_file.write(html)
                html_file.write("\n")

print(f"\n¡Éxito! Todas las imágenes procesadas fueron guardadas en un solo archivo: {html_output_path}")

