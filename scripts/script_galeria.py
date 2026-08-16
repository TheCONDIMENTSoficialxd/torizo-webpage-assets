import os
from PIL import Image
import urllib.parse

# 1. Configura la URL base de tu GitHub
BASE_URL = "https://raw.githubusercontent.com/TheCONDIMENTSoficialxd/torizo-webpage-assets/main/galeria/"

# 2. Configura el tag que llevarán estas imágenes
TAG = "tag"

# Recorrer todos los archivos en la carpeta actual
for i, filename in enumerate(os.listdir("."), start=1):
    # Filtrar solo archivos de imagen
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        
        # Abrir la imagen y obtener su tamaño original
        try:
            with Image.open(filename) as img:
                width, height = img.size
        except Exception as e:
            print(f"<!-- Error leyendo {filename}: {e} -->")
            continue
            
        # Formatear variables para el HTML
        # urllib.parse.quote asegura que los espacios se conviertan en %20 para la URL
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
