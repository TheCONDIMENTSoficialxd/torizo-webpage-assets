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
# PLANTILLAS HTML
# ==========================================

HTML_HEADER = '''<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GALERIA</title>

    <link rel="icon" href="https://raw.githubusercontent.com/TheCONDIMENTSoficialxd/torizo-webpage-assets/refs/heads/main/favicon.ico" type="image/x-icon" />
    <link rel="stylesheet" href="gallery.css" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bigger-picture@1.1.19/dist/bigger-picture.min.css" />
  </head>
  <body>
    <main>
      <main-divider>
        <hgroup>
          <h1 class="site-title">GALERIA DE ARTE</h1>

          <p class="label">filtra por categoria:</p>

          <div id="filters">
            <details-content class="filters">
              <div class="button-group" data-filter-group="type">
                <button class="button is-checked" data-filter="">todos</button>
                <button class="button" data-filter=".tag1">conceptual</button>
                <button class="button" data-filter=".tag2">paisajes</button>
                <button class="button" data-filter=".tag3">autorretratos</button>
                <button class="button" data-filter=".tag4">posters</button>
              </div>
            </details-content>
          </div>

          <hr />

          <nav class="nav-links">
            <a href="/" class="internal-link">&gt;&gt; VOLVER &lt;&lt;</a>
          </nav>
        </hgroup>

        <ul class="gallery grid" id="gallery">
          <div class="grid-sizer"></div>
          <div class="gutter-sizer"></div>
'''

HTML_FOOTER = '''        </ul>
      </main-divider>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bigger-picture@1.1.19/dist/bigger-picture.min.js"></script>
    <script defer>
      let bp = BiggerPicture({ target: document.body });
      let imageLinks = document.querySelectorAll("#gallery li > figure > a");

      let openGallery = function (e) {
        e.preventDefault();
        bp.open({
          items: imageLinks,
          el: e.currentTarget,
          intro: "fadeup",
          inline: false,
        });
      };
      for (let link of imageLinks) {
        link.addEventListener("click", openGallery);
      }
    </script>

    <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js"></script>
    <script defer>
      var iso = new Isotope(".grid", {
        itemSelector: ".grid-item",
        percentPosition: true,
        layoutMode: "masonry",
        masonry: {
          columnWidth: ".grid-sizer",
          gutter: ".gutter-sizer",
        },
      });

      function concatValues(obj) {
        var value = "";
        for (var prop in obj) {
          value += obj[prop];
        }
        return value;
      }

      var filters = {};
      var filtersElem = document.querySelector(".filters");
      filtersElem.addEventListener("click", function (event) {
        var isButton = event.target.classList.contains("button");
        if (!isButton) return;

        var buttonGroup = fizzyUIUtils.getParent(event.target, ".button-group");
        var filterGroup = buttonGroup.getAttribute("data-filter-group");
        filters[filterGroup] = event.target.getAttribute("data-filter");
        var filterValue = concatValues(filters);
        iso.arrange({ filter: filterValue });
      });

      var buttonGroups = document.querySelectorAll(".button-group");
      for (var i = 0; i < buttonGroups.length; i++) {
        var buttonGroup = buttonGroups[i];
        var onButtonGroupClick = getOnButtonGroupClick(buttonGroup);
        buttonGroup.addEventListener("click", onButtonGroupClick);
      }

      function getOnButtonGroupClick(buttonGroup) {
        return function (event) {
          var isButton = event.target.classList.contains("button");
          if (!isButton) return;
          buttonGroup.querySelector(".is-checked").classList.remove("is-checked");
          event.target.classList.add("is-checked");

          setTimeout(function () {
            imageLinks = document.querySelectorAll(
              '#gallery li:not([style*="display: none"]) > figure > a'
            );
          }, 550);
        };
      }
    </script>
  </body>
</html>
'''

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
    # Escribir la cabecera (Header) del HTML
    html_file.write(HTML_HEADER)
    
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
                
                # Bloque HTML para el elemento actual (Con la indentación correcta)
                html_li = f'''          <li class="grid-item entry {tag_id}" id="{html_id}">
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
          </li>\n'''
                
                # Escribir en el archivo
                html_file.write(html_li)
                
    # Escribir el pie de página (Footer con los scripts)
    html_file.write(HTML_FOOTER)

print(f"\n¡Éxito! El archivo 'index.html' completo ha sido generado y está listo para producción en: {html_output_path}")
