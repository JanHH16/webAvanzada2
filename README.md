# Laboratorio 2: Web Scraping, procesamiento y recuperacion de informacion

Ingenieria Web Avanzada | OII436-1

- Integrantes: Jan Houter y Camila Torres
- Repositorio: https://github.com/JanHH16/webAvanzada2

## Entorno virtual

Crear el entorno:

```
py -m venv .venv
```

Activar (PowerShell):

```
.venv\Scripts\Activate.ps1
```

Activar (CMD):

```
.venv\Scripts\activate.bat
```

## Reproducir la ejecucion desde un entorno nuevo

```
git clone https://github.com/JanHH16/webAvanzada2.git
cd webAvanzada2
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Orden de ejecucion:

```
python scraper.py
python procesamiento.py
python buscador.py
```

- `scraper.py`: extrae titulo, precio, disponibilidad y calificacion de la primera pagina de https://books.toscrape.com/.
- `procesamiento.py`: limpia los datos, crea `titulo_normalizado` y genera `libros.csv`.
- `buscador.py`: indice TF-IDF sobre `titulo_normalizado` y busqueda por similitud del coseno.

Gestion de elementos sin datos: si un libro no tiene algun campo o tiene un formato inesperado, `scraper.py` lo omite, imprime un aviso y continua con el siguiente.

## Evidencias

- Libros extraidos: 20
- Precio promedio: 38.05

Ejemplos de busqueda (con `top_k=3`):

Consulta `life`:

```
Scott Pilgrim's Precious Little Life (Scott Pilgrim #1) | Precio: 52.29 | Similitud: 0.2459
The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull | Precio: 17.93 | Similitud: 0.2250
Our Band Could Be Your Life: Scenes from the American Indie Underground, 1981-1991 | Precio: 57.25 | Similitud: 0.2231
```

Consulta `the`:

```
The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull | Precio: 17.93 | Similitud: 0.4181
The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics | Precio: 22.6 | Similitud: 0.3630
The Black Maria | Precio: 52.15 | Similitud: 0.3282
```

Comparacion del orden: en `the`, el primer titulo contiene la palabra tres veces, lo que aumenta su frecuencia de termino, y es el de mayor similitud. Los titulos con una sola aparicion quedan despues y pueden empatar (0.3282) cuando el resto de sus palabras tiene el mismo peso. En `life` la palabra aparece una vez en cada titulo, asi que el orden depende de los pesos TF-IDF de las demas palabras de cada uno, no solo de su longitud.

Desafio breve: se cambio la llamada a `buscar(consulta, top_k=3)` y el programa devuelve como maximo tres resultados con similitud positiva.

## Pruebas funcionales (Paso 12)

| Caso | Consulta utilizada | Resultado observado | Estado |
|---|---|---|---|
| T1 | life | Se recuperaron 3 libros ordenados de mayor a menor similitud (0.2459, 0.2250, 0.2231). | Cumple |
| T2 | zzxyz123 | Se mostro "No se encontraron coincidencias." | Cumple |
| T3 | LIFE | Se obtuvieron los mismos 3 libros, con las mismas similitudes y el mismo orden que en T1. | Cumple |
| T4 | (vacia) | Se mostro "Ingrese una consulta no vacia." y luego "No se encontraron coincidencias.", sin excepcion. | Cumple |

Observacion: en T4 aparecen dos mensajes porque `buscar` imprime el aviso y devuelve una lista vacia, y luego el bloque principal imprime el mensaje de sin coincidencias.

## Respuestas
