import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

file_path = "Support_DB_EDA_ready.csv"
df = pd.read_csv(file_path)

print("=== EDA Visual ===")
print("Dataset cargado con shape:", df.shape)


# 1. Visualización de nulos
plt.figure(figsize=(12, 5))
sns.heatmap(df.isna(), cbar=False, cmap="viridis")
plt.title("Mapa de valores nulos", fontsize=14)
plt.show()


# 2. Variables categóricas
categorical_cols = [
    "day_of_week", "priority", "industry", "region", "product_area", "customer_tier"
]

for col in categorical_cols:
    if col in df.columns:
        plt.figure(figsize=(8, 5))
        order = df[col].value_counts().index
        sns.countplot(data=df, x=col, order=order, palette="Set2")
        plt.title(f"Distribución de {col}", fontsize=14)
        plt.xticks(rotation=30)
        plt.show()

# 3. Variables numéricas
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

for col in numeric_cols:
    plt.figure(figsize=(12, 5))
    
    # Histograma
    plt.subplot(1, 2, 1)
    sns.histplot(df[col].dropna(), kde=True, bins=30, color="skyblue")
    plt.title(f"Histograma de {col}")
    
    # Boxplot
    plt.subplot(1, 2, 2)
    sns.boxplot(x=df[col], color="lightcoral")
    plt.title(f"Boxplot de {col}")
    
    plt.suptitle(f"Análisis de {col}", fontsize=14)
    plt.show()


# 4. Correlación numérica
if len(numeric_cols) > 1:
    plt.figure(figsize=(10, 7))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de correlación entre variables numéricas", fontsize=14)
    plt.show()

print("EDA visual finalizado ✅")