"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os

def pregunta_01():
    df = pd.read_csv(
        "files/input/solicitudes_de_credito.csv",
        sep=";"
    )

    df = (
        df.drop(columns=["Unnamed: 0"])
          .dropna()
          .drop_duplicates()
    )

    df[["día", "mes", "año"]] = (
        df["fecha_de_beneficio"]
        .str.split("/", expand=True)
    )

    mask = df["año"].str.len() < 4

    df.loc[mask, ["día", "año"]] = (
        df.loc[mask, ["año", "día"]].values
    )

    df["fecha_de_beneficio"] = (
        df["año"]
        + "-"
        + df["mes"]
        + "-"
        + df["día"]
    )

    df = df.drop(columns=["día", "mes", "año"])

    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "línea_credito",
    ]

    df[columnas_texto] = (
        df[columnas_texto]
        .apply(
            lambda col:
                col.str.lower()
                   .str.replace("-", " ", regex=False)
                   .str.replace("_", " ", regex=False)
                   .str.strip()
        )
    )

    df['barrio'] = df['barrio'].str.lower().replace(['-', '_'], ' ', regex=True) 

    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["monto_del_credito"] = (
        pd.to_numeric(
            df["monto_del_credito"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
        .astype(str)
    )

    df = df.drop_duplicates()

    os.makedirs(
        "files/output",
        exist_ok=True
    )

    df.to_csv(
        "files/output/solicitudes_de_credito.csv",
        sep=";",
        index=False
    )

    return df.head()
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
