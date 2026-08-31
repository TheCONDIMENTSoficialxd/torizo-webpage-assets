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
    """
    Función de apoyo para autocompletar rutas usando la tecla TAB (estilo Fish/Bash).
    """
    # Expandir virgulilla (~) si se usa en la ruta
    text = os.path.expanduser(text)
    
    if os.path.isdir(text):
        # Si es un directorio válido, listar su contenido
        dir_path = text
        prefix = ""
    else:
        # Si está escribiendo parcialmente una ruta, separar directorio y prefijo
        dir_path, prefix = os.path.split(text)
        if not dir_path:
            dir_path = "."

    try:
        # Obtener todos los elementos que coincidan
        items = os.listdir(dir_path)
    except OSError:
        return None

    # Filtrar solo los que comiencen con el prefijo actual
    matches = [
        os.path.join(dir_path, item) if dir_path != "." else item
        for item in items if item.startswith(prefix)
    ]
    
    # Agregar barra diagonal si es un directorio para seguir explorando
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

# Configurar el autocompletado en la terminal
if readline:
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    # Configurar la función de completado
    readline.set_completer(completar_rutas)

# ==========================================
# INICIO DEL SCRIPT PRINCIPAL
# ==========================================

# 1. Configura la URL base general de tu GitHub (sin la carpeta final del tag)
BASE_URL_GENERAL = "https://raw.githubusercontent.com/TheCONDIMENTSoficialxd/torizo-webpage-assets/main/galeria/"

print("--- Generador de HTML para Galería ---")
print("Tip: Usa la tecla [TAB] para autocompletar rutas de carpetas.\n")

# 2. Pedir al usuario la ubicación con soporte de autocompletado
folder = input("Introduce la ruta de la carpeta donde están las imágenes: ").strip()
folder = os.path.expanduser(folder) # Limpiar formato de ruta si usa ~

# Comprobar que la carpeta existe
if not os.path.isdir(folder):
    print(f"\nError: la carpeta '{folder}' no existe o no es válida.")
    exit()

# 3. Mostrar los tags disponibles
tags = {
    "1": "conceptual",
    "2": "paisajes",
    "3": "autorretratos",
    "4": "posters"
}

print("\nTags disponibles:")
for numero, nombre in tags.items():
    print(f"  {numero} = {nombre}")

# 4. Pedir al usuario el número del tag
tag_input = input("\nSelecciona el número del tag: ").strip()

# Comprobar que el número sea válido
if tag_input not in tags:
    print("Error: debes seleccionar 1, 2, 3 o 4.")
    exit()

# El HTML utilizará tag1, tag2, tag3 o tag4
TAG = f"tag{tag_input}"
NOMBRE_TAG = tags[tag_input]

# Construir la URL base final incluyendo la subcarpeta del tag seleccionado
BASE_URL = f"{BASE_URL_GENERAL}{NOMBRE_TAG}/"

print(f"\nTag seleccionado: {TAG} ({NOMBRE_TAG})")
print(f"URL Base generada: {BASE_URL}\n")
print("-" * 40 + "\n")

# 5. Recorrer todos los archivos en la carpeta seleccionada
for i, filename in enumerate(os.listdir(folder), start=1):

    # Filtrar solo archivos de imagen
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):

        # Ruta completa de la imagen
        filepath = os.path.join(folder, filename)

        # Abrir la imagen y obtener su tamaño original
        try:
            with Image.open(filepath) as img:
                width, height = img.size
        except Exception as e:
            continue

        # Formatear variables para el HTML
        url = BASE_URL + urllib.parse.quote(filename)
        title = os.path.splitext(filename)[0]
        html_id = title.replace(" ", "-").lower()

        # Generar el HTML con las dimensiones exactas
        html = f'''<li class="grid-item entry {TAG}" id="{html_id}">
  <figure>
    <a
      href="{url}"
      data-img="{url}"
      data-thumb="{url}"
      data-alt="{title}"
      data-caption="{title}"
      data-width="{width}"
      data-height="{height}"
    >
      <img
        loading="lazy"
        class="responsive"
        width="{width}"
        height="{height}"
        src="{url}"
        alt="{title}"
      />
    </a>
    <figcaption class="caption">{title}</figcaption>
  </figure>
</li>'''

        print(html)
        print("\n")
