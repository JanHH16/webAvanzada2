import pandas as pd

from scraper import obtener_libros


def procesar():
    # Paso 5: DataFrame a partir de la lista de diccionarios
    libros = obtener_libros()
    df = pd.DataFrame(libros)

    print(df.head())
    print(df.info())
    print(df.shape)
    print(df.columns.tolist())

    # Paso 6: limpieza
    df["titulo"] = df["titulo"].astype(str).str.strip()
    df = df.drop_duplicates(subset="titulo").reset_index(drop=True)
    df["titulo_normalizado"] = df["titulo"].str.lower()

    # Verificar tipos numericos (errors="raise": falla si hay un valor no numerico)
    df["precio"] = pd.to_numeric(df["precio"]).astype(float)
    df["calificacion"] = pd.to_numeric(df["calificacion"]).astype(int)
    print(df.dtypes)

    # Paso 7: indicadores y exportacion
    cantidad = len(df)
    precio_promedio = df["precio"].mean()
    print(f"Cantidad de libros: {cantidad}")
    print(f"Precio promedio: {precio_promedio:.2f}")

    df.to_csv("libros.csv", index=False, encoding="utf-8")
    print("Archivo libros.csv generado")
    return df


if __name__ == "__main__":
    procesar()
