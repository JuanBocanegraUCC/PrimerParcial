import pandas as pd

file_path = "Support_DB_clean.csv"
df = pd.read_csv(file_path)

# ---- Normalizar nombres de columnas AL INICIO ----
# quitar BOM, trim, pasar a minúsculas, reemplazar espacios por guión bajo y eliminar caracteres raros
df.columns = (
    df.columns
    .astype(str)
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"[^\w]", "_", regex=True)
)

print("=== Archivo cargado ===")
print("Shape inicial:", df.shape)
print("Columnas (normalizadas):", df.columns.tolist())
print()

# ---- Contar y reemplazar '--' ----
# contamos sobre representación original (string) — convertir a str para evitar errores
conteo_guiones = (df.astype(str) == "--").sum().sum()
print(f"Valores '--' encontrados: {conteo_guiones}")

df = df.replace("--", pd.NA)
print(f"Valores '--' reemplazados por NaN: {conteo_guiones}")
print()

# ---- Duplicados ----
duplicados = df.duplicated().sum()
print(f"Duplicados encontrados: {duplicados}")
df = df.drop_duplicates()
print(f"Duplicados eliminados: {duplicados}")
print("Shape después de eliminar duplicados:", df.shape)
print()

# ---- Valores nulos ----
nulos = df.isna().sum()
total_nulos = int(nulos.sum())
print("=== Valores nulos por columna (top 15) ===")
print(nulos[nulos > 0].sort_values(ascending=False).head(15))
print(f"Total de valores nulos (incluyendo '--' reemplazados): {total_nulos}")
print()

# ---- Traducción day_of_week ----
translate_days = {
    "lun": "mon", "mar": "tue", "mie": "wed", "jue": "thu", "vie": "fri", "sab": "sat", "dom": "sun",
    "lunes": "mon", "martes": "tue", "miércoles": "wed", "miercoles": "wed", "jueves": "thu",
    "viernes": "fri", "sábado": "sat", "sabado": "sat", "domingo": "sun"
}

if "day_of_week" in df.columns:
    # normalizamos a minúsculas por seguridad
    before_counts = df["day_of_week"].astype(str).str.strip().value_counts(dropna=False)
    df["day_of_week"] = df["day_of_week"].astype(str).str.strip().str.lower().replace(translate_days)
    after_counts = df["day_of_week"].value_counts(dropna=False)
    # contar cambios exactos: comparar suma de coincidencias de valores de before vs after
    # mejor: contar cuántos valores en before estaban en español (heurístico sobre keys de translate_days)
    spanish_keys = set(translate_days.keys())
    num_spanish = df["day_of_week"].astype(str).str.strip().str.lower().isin(spanish_keys).sum()
    print(f"Traducciones aplicadas en 'day_of_week' (registros que eran español y se normalizaron): {num_spanish}")
    print("Distribución actualizada de day_of_week:")
    print(after_counts)
    print()

# ---- Contadores solicitados: company_id y product_area ----
if "company_id" in df.columns:
    print("\n=== Cantidad de tickets por empresa (company_id) ===")
    print(df["company_id"].value_counts().head(50))  # top 50 para consola

if "product_area" in df.columns:
    print("\n=== Cantidad de tickets por categoría (product_area) ===")
    print(df["product_area"].value_counts())
print()

# ---- Detección automática de columna de 'medio de recepción' ----
keywords = ["submitted", "submit", "channel", "source", "medium", "method", "intake", "received", "via", "origin"]
candidates = [c for c in df.columns if any(k in c for k in keywords)]

if candidates:
    # priorizar candidatas que contengan 'submitted' o 'submit'
    preferred = [c for c in candidates if "submitted" in c or "submit" in c]
    chosen = preferred[0] if preferred else candidates[0]
    print(f"Columna detectada como 'medio de recepción': '{chosen}' (candidatas: {candidates})")
    print("\n=== Cantidad de tickets por medio de recepción ===")
    print(df[chosen].value_counts(dropna=False))
    print("\n=== Medios de recepción disponibles ===")
    print(df[chosen].dropna().unique())
    print(f"Total de medios de recepción (no nulos): {int(df[chosen].nunique(dropna=True))}")
else:
    print("No se detectó automáticamente una columna de 'medio de recepción'.")
    print("Columnas candidatas revisadas:", df.columns.tolist())
    print("Si existe en el dataset, revisa su nombre exacto y ejecútalo manualmente, por ejemplo:")
    print("    print(df['submitted_via'].value_counts())  # si 'submitted_via' es la columna correcta")

# ---- Guardar CSV final ----
df.to_csv("Support_DB_EDA_ready.csv", index=False, encoding="utf-8-sig")
print("\nArchivo final guardado en: Support_DB_EDA_ready.csv")