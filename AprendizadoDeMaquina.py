# %%
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np
import requests
from collections import Counter

df = pd.read_csv("traefik.csv")
df = df.drop(columns=["data1","data2","tamanho"]) # ----------------- REMOVENDO COLUNAS DATA1, DATA2, TAMANHO ---------------------
df

# %%
def separandoString(linha):
    dividindo = linha.split("/")
    if len(dividindo) < 2:
        primeiraParte = dividindo[0]
    else:
        primeiraParte = dividindo[1]
    return primeiraParte


# %% Preparando o dataframe
coluna_status = df["status"]
coluna_racursos = df["recurso"]
recursos = coluna_racursos.apply(separandoString)
df["recurso"] = recursos
df_pronto = df.loc[df["status"] != 429]

# %%
