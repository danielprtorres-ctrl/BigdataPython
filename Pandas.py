import pandas as pd
import numpy as np

# =========================================
# LEITURA DA PLANILHA
# =========================================

arquivo = "PLANILHA2025.xlsx"

df = pd.read_excel(arquivo)

# =========================================
# USANDO OS NOMES ORIGINAIS
# =========================================

df.columns = [
    "MÊS AVISO",
    "DATA EVENTO",
    "MODELO SEG",
    "TIPO SINISTRO",
    "VEICULO",
    "UF",
    "LUCRO",
    "Valor"
]

# =========================================
# CONVERSÃO DAS DATAS
# =========================================

df["MÊS AVISO"] = pd.to_datetime(
    df["MÊS AVISO"],
    errors="coerce"
)

df["DATA EVENTO"] = pd.to_datetime(
    df["DATA EVENTO"],
    errors="coerce"
)

# =========================================
# MÉDIA ENTRE AS DATAS
# =========================================

diferenca = (
    df["DATA EVENTO"] -
    df["MÊS AVISO"]
) / 2

df["DATA MEDIA"] = (
    df["MÊS AVISO"] +
    diferenca
)

# =========================================
# AJUSTE DOS VALORES
# =========================================

df["LUCRO"] = pd.to_numeric(
    df["LUCRO"],
    errors="coerce"
)

df["Valor"] = pd.to_numeric(
    df["Valor"],
    errors="coerce"
)

# =========================================
# PADRONIZAÇÃO DOS TEXTOS
# =========================================

for coluna in [
    "MODELO SEG",
    "TIPO SINISTRO",
    "VEICULO",
    "UF"
]:

    df[coluna] = (
        df[coluna]
        .astype(str)
        .str.strip()
        .str.title()
    )

# =========================================
# REMOVER DUPLICATAS
# =========================================

df = df.drop_duplicates()

# =========================================
# REMOVER LINHAS VAZIAS
# =========================================

df = df.dropna(how="all")

# =========================================
# DADO SIMULADO
# PREVISÃO DE LUCRO
# =========================================

lucro_mensal = (
    df.groupby(
        df["DATA MEDIA"]
        .dt.to_period("M")
    )["LUCRO"]
    .sum()
    .reset_index()
)

# Converter para texto
lucro_mensal["DATA MEDIA"] = (
    lucro_mensal["DATA MEDIA"]
    .astype(str)
)

# Índice numérico
lucro_mensal["Indice"] = range(
    len(lucro_mensal)
)

# Regressão linear
coeficientes = np.polyfit(
    lucro_mensal["Indice"],
    lucro_mensal["LUCRO"],
    1
)

# =========================================
# PREVISÃO DOS PRÓXIMOS 4 MESES
# =========================================

ultimo_indice = (
    lucro_mensal["Indice"]
    .max()
)

ultima_data = pd.Period(
    lucro_mensal["DATA MEDIA"].iloc[-1],
    freq="M"
)

previsoes = []

for i in range(1, 5):

    novo_indice = ultimo_indice + i

    lucro_previsto = (
        coeficientes[0] *
        novo_indice
        + coeficientes[1]
    )

    previsoes.append({

        "MES_PREVISAO": str(
            ultima_data + i
        ),

        "LUCRO_PREVISTO": round(
            lucro_previsto,
            2
        )
    })

# =========================================
# DATAFRAME DE PREVISÃO
# =========================================

df_previsao = pd.DataFrame(
    previsoes
)

# =========================================
# EXPORTAÇÃO
# =========================================

df.to_excel(
    "BASE_BIGDATA_SEGURADORA.xlsx",
    index=False
)

df_previsao.to_excel(
    "PREVISAO_LUCRO.xlsx",
    index=False
)

# =========================================
# RESULTADOS
# =========================================

print("\nBASE TRATADA:")
print(df.head())

print("\nPREVISÃO DE LUCRO:")
print(df_previsao)

print("\nPROCESSAMENTO FINALIZADO.")
