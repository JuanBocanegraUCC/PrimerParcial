import pandas as pd

file_path = "Support_DB_clean.csv"
df = pd.read_csv(file_path)

print("=== Archivo cargado ===")
print("Shape:", df.shape)
print("Columnas:", df.columns.tolist())
print()

df = df.replace("--", pd.NA)

# Detectar si hay valores en español y mapearlos a inglés
translate_days = {
    "Lun": "Mon",
    "Mar": "Tue",
    "Mie": "Wed",
    "Jue": "Thu",
    "Vie": "Fri",
    "Sab": "Sat",
    "Dom": "Sun",
    "Lunes": "Mon",
    "Martes": "Tue",
    "Miércoles": "Wed",
    "Jueves": "Thu",
    "Viernes": "Fri",
    "Sábado": "Sat",
    "Domingo": "Sun"
}

if "day_of_week" in df.columns:
    df["day_of_week"] = df["day_of_week"].replace(translate_days)


# Valores nulos
print("=== Valores nulos por columna (top 10) ===")
print(df.isna().sum().sort_values(ascending=False).head(10))
print()

# Distribuciones claves
def top_counts(col, n=10):
    if col in df.columns:
        print(f"--- Top valores en '{col}' ---")
        print(df[col].value_counts().head(n))
        print()

for col in ["priority", "industry", "region", "product_area", "customer_tier"]:
    top_counts(col)

# Resumen numérico
print("=== Resumen estadístico (numéricas) ===")
print(df.describe())
print()

df.to_csv("Support_DB_EDA_ready.csv", index=False)
print("Archivo final guardado en: Support_DB_EDA_ready.csv")
