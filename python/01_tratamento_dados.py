from pysus import sih

# TESTE: só 1 mês, de 1 estado
df = sih(
    state="SP",
    year=2024,
    month=[1],
    as_dataframe=True
)

print("Formato do DataFrame (linhas, colunas):", df.shape)
print(df.head())

# Salva localmente
df.to_parquet("dados_brutos_sih.parquet")

print("Arquivo salvo: dados_brutos_sih.parquet")

import pandas as pd

# Carrega os dados brutos
df = pd.read_parquet("dados_brutos_sih.parquet")

print("Linhas antes da limpeza:", len(df))

# Seleciona apenas as colunas necessárias
colunas_uteis = [
    "N_AIH",
    "MUNIC_RES",
    "DT_INTER",
    "DIAS_PERM",
    "VAL_TOT"
]

df = df[colunas_uteis].copy()

# Padroniza os tipos
df["DT_INTER"] = pd.to_datetime(
    df["DT_INTER"],
    format="%Y%m%d",
    errors="coerce"
)

df["VAL_TOT"] = pd.to_numeric(
    df["VAL_TOT"],
    errors="coerce"
)

df["DIAS_PERM"] = pd.to_numeric(
    df["DIAS_PERM"],
    errors="coerce"
)

print("Nulos por coluna:")
print(df.isna().sum())

# Remove registros sem data ou município
df = df.dropna(
    subset=["DT_INTER", "MUNIC_RES"]
)

# Remove duplicados
df = df.drop_duplicates(
    subset=["N_AIH"]
)

print("Linhas depois da limpeza:", len(df))
print(
    "Período coberto:",
    df["DT_INTER"].min(),
    "até",
    df["DT_INTER"].max()
)

print(
    "Municípios distintos:",
    df["MUNIC_RES"].nunique()
)

# Salva o resultado tratado
df.to_parquet(
    "dados_tratados_sih.parquet"
)

print(
    "Arquivo salvo: dados_tratados_sih.parquet"
)

import oracledb
from dotenv import load_dotenv
import os

load_dotenv()

conn = oracledb.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dsn=os.getenv("DB_DSN"),
    config_dir="./wallet",
    wallet_location="./wallet",
    wallet_password=os.getenv("WALLET_PASSWORD")
)

print("Conectado com sucesso!")

conn.close()

import oracledb
from dotenv import load_dotenv
import os

load_dotenv()

conn = oracledb.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dsn=os.getenv("DB_DSN"),
    config_dir="./wallet",
    wallet_location="./wallet",
    wallet_password=os.getenv("WALLET_PASSWORD")
)

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM STG_INTERNACOES"
)

print(
    "Total de registros no banco:",
    cursor.fetchone()[0]
)

cursor.execute(
    """
    SELECT
        MIN(DT_INTERNACAO),
        MAX(DT_INTERNACAO)
    FROM STG_INTERNACOES
    """
)

print(
    "Período no banco:",
    cursor.fetchone()
)

conn.close()
