import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

# Las calificaciones vienen como palabra en la clase CSS (ej. "star-rating Three")
CALIFICACIONES = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def obtener_libros():
    """Extrae titulo, precio, disponibilidad y calificacion de la primera pagina."""
    respuesta = requests.get(URL, timeout=10)
    respuesta.raise_for_status()
    # El sitio no declara la codificacion; se fuerza UTF-8 para que el simbolo de libra no se corrompa
    respuesta.encoding = "utf-8"
    soup = BeautifulSoup(respuesta.text, "html.parser")

    libros = []
    for articulo in soup.select("article.product_pod"):
        try:
            titulo = articulo.h3.a["title"].strip()
            precio_texto = articulo.select_one("p.price_color").get_text(strip=True)
            precio = float(precio_texto.replace("£", ""))
            disponibilidad = articulo.select_one("p.availability").get_text(strip=True)
            clases = articulo.select_one("p.star-rating")["class"]
            calificacion = next(CALIFICACIONES[c] for c in clases if c in CALIFICACIONES)
        except (AttributeError, KeyError, TypeError, ValueError, StopIteration) as error:
            # Elemento sin datos o con formato inesperado: se omite ese libro y se continua
            print(f"Libro omitido por datos incompletos: {error!r}")
            continue

        libros.append({
            "titulo": titulo,
            "precio": precio,
            "disponibilidad": disponibilidad,
            "calificacion": calificacion,
        })
    return libros


if __name__ == "__main__":
    libros = obtener_libros()
    print(f"Total extraido: {len(libros)}")
    for libro in libros[:5]:
        print(libro)
