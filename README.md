# Laboratorio 2: Web Scraping, procesamiento y recuperacion de informacion

Ingenieria Web Avanzada | OII436-1

- Integrantes: Jan Houter y Camila Torres

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

**Pregunta 1: ¿Para qué sirve BeautifulSoup y cómo se diferencia de requests?**  
BeautifulSoup es una librería de Python orientada al análisis y procesamiento de estructuras HTML y XML, que facilita la navegación e inspección del árbol DOM para extraer datos específicos mediante selectores. La diferencia fundamental es que `requests` se limita a gestionar la comunicación HTTP enviando peticiones y descargando la respuesta del servidor, mientras que BeautifulSoup toma el código HTML resultante y permite filtrar e interrogar sus elementos.

**Pregunta 2: ¿Qué riesgo existe al depender de selectores HTML específicos si el sitio cambia?**  
El principal riesgo radica en la fragilidad y acoplamiento del *scraper* con la estructura del sitio web. Si los desarrolladores de la página modifican el diseño, cambian las clases CSS, los identificadores o la jerarquía de las etiquetas HTML, los selectores definidos dejarán de encontrar los elementos objetivo, ocasionando errores en la ejecución o la extracción de registros vacíos e incompletos.

**Pregunta 3: ¿Por qué normalizar los títulos antes de implementar la búsqueda?**  
Garantiza que la búsqueda no falle por variaciones ortográficas superficiales, como el uso de mayúsculas o espacios extra, permitiendo que las consultas de los usuarios coincidan de forma consistente con los títulos indexados.

**Pregunta 4: En el código entregado, ¿qué función cumple `fit_transform()` sobre los títulos y por qué se usa `transform()` para la consulta?**  
En los títulos, la función `fit_transform()` cumple un doble propósito: primero analiza la colección completa para aprender el vocabulario de términos únicos y luego genera la matriz numérica TF-IDF. Para la consulta ingresada por el usuario se utiliza únicamente `transform()`, ya que esta debe ser proyectada en el espacio vectorial existente usando exactamente el mismo vocabulario previamente aprendido. Si aplicáramos `fit_transform()` a la consulta, se redefiniría el vocabulario a partir de esa sola frase, rompiendo la dimensión vectorial y haciendo imposible calcular la similitud con la matriz de títulos.

**Pregunta 5: Si dos libros obtienen similitudes de 0.75 y 0.20 para la misma consulta, ¿cuál se muestra primero? Explique qué indica una puntuación cercana a cero.**  
Se muestra primero el libro con similitud 0.75, porque el sistema ordena los resultados de mayor a menor similitud del coseno. Una puntuacion cercana a 0 indica que la consulta y el titulo comparten muy pocos términos del vocabulario, o ninguno si es exactamente 0. Esto no significa que los textos no estén relacionados por significado, solo que no coinciden por palabras.
 
**Pregunta 6: ¿Qué limitación tiene buscar solo por palabras presentes en títulos mediante TF-IDF? Proponga una mejora concreta.**  
La mayor limitación del enfoque TF-IDF aplicado exclusivamente a títulos es que depende de la coincidencia exacta de palabras clave en un texto muy breve, sin comprender la semántica, sinónimos ni el contexto del libro. Como mejora concreta, se propone ampliar el índice agregando la sinopsis o descripción completa de las obras, o bien migrar a un modelo de búsqueda semántica mediante *embeddings* de texto (como SBERT), lo que permitiría recuperar libros por afinidad conceptual aunque no compartan exactamente los mismos términos.
