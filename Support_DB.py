import pandas as pd
from pathlib import Path

file_path = "Support_DB(in).csv"
out_path = "Support_DB_clean.csv"

def parse_mixed_delimiter(path):
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n\r")
            if not line:
                continue
            # Buscamos la primera ocurrencia de '|' (separador que marca el límite
            # entre las primeras 3 columnas (con coma) y el resto (con pipe))
            first_pipe = line.find("|")
            if first_pipe == -1:
                parts = [p.strip() for p in line.split(",")]
                rows.append(parts)
                continue

            left = line[:first_pipe]         # contiene las 3 primeras columnas separadas por ','
            right = line[first_pipe + 1:]    # contiene el resto separado por '|'

            left_parts = [p.strip() for p in left.split(",")]
            right_parts = [p.strip() for p in right.split("|")]

            combined = left_parts + right_parts
            rows.append(combined)

    maxlen = max(len(r) for r in rows)
    rows = [r + [""] * (maxlen - len(r)) for r in rows]

    header = rows[0]
    data = rows[1:]

    # Crear DataFrame
    df = pd.DataFrame(data, columns=header)

    # Normalizar nombres de columnas (quitar BOM, espacios)
    df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]

    return df

def postprocess(df):
    if "ticket_id" in df.columns:
        df["ticket_id"] = pd.to_numeric(df["ticket_id"], errors="coerce")
    if "day_of_week_num" in df.columns:
        df["day_of_week_num"] = pd.to_numeric(df["day_of_week_num"], errors="coerce")
    for col in ["company_id", "past_30d_tickets", "past_90d_incidents", "org_users",
                "customers_affected", "error_rate_pct", "downtime_min"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].str.replace(",", "."), errors="coerce")

    empty_cols = [c for c in df.columns if df[c].eq("").all() or df[c].isna().all()]
    if empty_cols:
        print("Eliminando columnas vacías:", empty_cols)
        df = df.drop(columns=empty_cols)

    return df

def brief_eda(df, n_show=5):
    print("\n--- Resumen rápido ---")
    print("Shape:", df.shape)
    print("Columnas:", df.columns.tolist())
    print("\nPrimeras filas:")
    print(df.head(n_show))
    print("\nValores nulos por columna (top 10):")
    print(df.isnull().sum().sort_values(ascending=False).head(10))
    # Mostrar distribución de algunas categóricas si existen
    for col in ("priority", "industry", "region", "product_area", "customer_tier"):
        if col in df.columns:
            print(f"\nTop 10 valores en '{col}':")
            print(df[col].value_counts(dropna=False).head(10))

def main():
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"No encontré el archivo {file_path} en el directorio actual.")

    print("Leyendo y parseando el archivo (mezcla de ',' y '|') ...")
    df = parse_mixed_delimiter(file_path)

    print("Post-procesando columnas (conversión de tipos, limpieza) ...")
    df = postprocess(df)

    # Guardar CSV limpio
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"CSV limpio guardado en: {out_path}")

    # Mostrar EDA rápido
    brief_eda(df)

if __name__ == "__main__":
    main()