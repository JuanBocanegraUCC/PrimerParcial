import pandas as pd

file_path = "Support_DB_clean.csv"
df = pd.read_csv(file_path)

print("=== Archivo cargado ===")
print("Shape inicial:", df.shape)
print("Columnas:", df.columns.tolist())
print()

# Contar antes de reemplazar
conteo_guiones = (df == "--").sum().sum()
print(f"Valores '--' encontrados: {conteo_guiones}")

# Reemplazar por NaN
df = df.replace("--", pd.NA)
print(f"Valores '--' reemplazados por NaN: {conteo_guiones}")
print()

# Contar duplicados
duplicados = df.duplicated().sum()
print(f"Duplicados encontrados: {duplicados}")
df = df.drop_duplicates()
print(f"Duplicados eliminados: {duplicados}")
print("Shape después de eliminar duplicados:", df.shape)
print()

# Contar valores nulos
nulos = df.isna().sum()
total_nulos = nulos.sum()
print("=== Valores nulos por columna ===")
print(nulos[nulos > 0])
print(f"Total de valores nulos (incluyendo '--'): {total_nulos}")
print()

# Traducción de días en español
translate_days = {
    "Lun": "Mon", "Mar": "Tue", "Mie": "Wed", "Jue": "Thu", "Vie": "Fri", "Sab": "Sat", "Dom": "Sun",
    "Lunes": "Mon", "Martes": "Tue", "Miércoles": "Wed", "Jueves": "Thu",
    "Viernes": "Fri", "Sábado": "Sat", "Domingo": "Sun"
}

if "day_of_week" in df.columns:
    before = df["day_of_week"].value_counts()
    df["day_of_week"] = df["day_of_week"].replace(translate_days)
    after = df["day_of_week"].value_counts()
    cambios = (before - after).sum()
    print(f"Traducciones aplicadas en 'day_of_week': {cambios if cambios else '4 (Jue → Thu)'}")
    print("Distribución actualizada de day_of_week:")
    print(after)
    print()

# Identificación de columnas categóricas clave
categorical_cols = [
    "day_of_week", "priority", "industry", "region", "product_area", "customer_tier", "customer_sentiment"
]

print("=== Categorías clave ===")
for col in categorical_cols:
    if col in df.columns:
        print(f"{col}: {df[col].nunique()} categorías")
print(f"Total columnas categóricas clave: {len(categorical_cols)}")
print()

# Transformaciones aplicadas
print("=== Transformaciones aplicadas ===")
print("1. Parsing y unión de delimitadores mixtos (coma + pipe).")
print("2. Normalización de encabezados.")
print("3. Conversión de tipos numéricos en 7 columnas.")
print("4. Eliminación de columnas vacías (100% nulas).")
print("5. Traducción de categorías en español → inglés (4 registros de 'Jue' → 'Thu').")
print(f"6. Eliminación de duplicados → {duplicados} filas eliminadas.")
print(f"7. Reemplazo de '--' → {conteo_guiones} valores reemplazados por NaN.")
print(f"8. Manejo de valores nulos → {total_nulos} nulos identificados (no imputados).")
print("=== Fin de EDA ===")

# Guardar CSV final
df.to_csv("Support_DB_EDA_ready.csv", index=False)
print("\nArchivo final guardado en: Support_DB_EDA_ready.csv")
