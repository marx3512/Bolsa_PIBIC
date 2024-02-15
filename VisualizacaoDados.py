# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from collections import Counter

df = pd.read_csv("traefik.csv")
df

# %%
# Refazendo coisas
tipoStatus = df["status"].unique()  # 0:200 1:404 2:429
status200 = df[df["status"] == tipoStatus[0]]
status404 = df[df["status"] == tipoStatus[1]]
status429 = df[df["status"] == tipoStatus[2]]

metodos404 = status404["metodo"].unique()  # 0:GET 1:POST 2:HEAD 3:OPTIONS 4:PUT 5:PATCH 6:CONNECT
GET404 = status404[status404["metodo"] == metodos404[0]]
POST404 = status404[status404["metodo"] == metodos404[1]]
HEAD404 = status404[status404["metodo"] == metodos404[2]]
PUT404 = status404[status404["metodo"] == metodos404[3]]
PATCH404 = status404[status404["metodo"] == metodos404[4]]
CONNECT404 = status404[status404["metodo"] == metodos404[5]]
print("GET404: " + str(len(GET404)))
print("POST404: " + str(len(POST404)))
print("HEAD404: " + str(len(HEAD404)))
print("PUT404: " + str(len(PUT404)))
print("PATCH404: " + str(len(PATCH404)))
print("CONNECT404: " + str(len(CONNECT404)))

totalVar = len(GET404) + len(POST404) + len(HEAD404) + len(PUT404) + len(PATCH404) + len(CONNECT404)
print("Quantidade total somando variaveis: " + str(totalVar))
print("Total 404: " + str(len(status404)))


# %%

metodos429 = status429["metodo"].unique()  # 0:GET 1:POST
GET429 = status429[status429["metodo"] == metodos429[0]]
POST429 = status429[status429["metodo"] == metodos429[1]]
print("GET404: " + str(len(GET429)))
print("POST404: " + str(len(POST429)))

total429 = len(GET429) + len(POST429)
print("Quantidade total somando variaveis: " + str(total429))
print("Total 429: " + str(len(status429)))

# %% Testando a separação da string
def separandoString(linha):
    recursoString = linha["recurso"]
    dividindo = recursoString.split("/")
    if len(dividindo) < 2:
        primeiraParte = dividindo[0]
    else:
        primeiraParte = dividindo[1]
    return primeiraParte

# %% Pegando quantidade de ip`s entre cada metodo
ipPATCH404 = PATCH404["ip"].unique() # Ip`s no dataset PATCH404
jsonIpPATCH404 = []

for ip in ipPATCH404:
    ipPatch = PATCH404[PATCH404["ip"] == ip] #Pegando todos os ip`s que est'ao no dataset PATCH404
    quantidade = np.count_nonzero(PATCH404["ip"] == ip) #Pegando quantidade de ip`s
    recursos = ipPatch.apply(separandoString, axis=1)
    primeiraParteRecurso = []
    for rec in recursos:
        primeiraParteRecurso.append(rec)

    infoQuantIP = {
        "ip": ip,
        "quantidade": quantidade,
        "recursos": primeiraParteRecurso
    }
    jsonIpPATCH404.append(infoQuantIP)

jsonIpPATCH404 = sorted(jsonIpPATCH404, key=lambda x: x["quantidade"], reverse=True) # Esta ordenando os ips
test = PATCH404[PATCH404["ip"] == jsonIpPATCH404[0]["ip"]]

#for ip in jsonIpPATCH404[:10]:
    #ipPatch = PATCH404[PATCH404["ip"] == ip]

print(jsonIpPATCH404[0]["ip"])

# %% Mostrando informações de forma organizada

def contabilizandoRecursos(recursos):
    contagem = Counter(recursos)
    jsonRecursos = []
    for elemento, quantidade in contagem.items():
        infoQuantRecurso = {
            "recurso": elemento,
            "quantidade": quantidade
        }
        jsonRecursos.append(infoQuantRecurso)

    jsonRecursos = sorted(jsonRecursos, key=lambda x: x["quantidade"], reverse=True) # Esta ordenando os recursos

    for info in jsonRecursos[:10]:
        print(f"recurso: {info['recurso']} quantidade:{info['quantidade']}")

def mostrarInfo(recursosDataSet):

    ipsUnicos = recursosDataSet["ip"].unique() # Ip`s no dataset PATCH404
    jsonIp = []

    for ip in ipsUnicos:
        ipPatch = recursosDataSet[recursosDataSet["ip"] == ip] #Pegando todos os ip`s que est'ao no dataset PATCH404
        quantidade = np.count_nonzero(recursosDataSet["ip"] == ip) #Pegando quantidade de ip`s
        recursos = ipPatch.apply(separandoString, axis=1) #Pegando a primeira palavra entra a primeira barra e a segunda
        response = requests.get(f'https://ipapi.co/{ip}/json/').json()
        primeiraParteRecurso = []
        for rec in recursos:
            primeiraParteRecurso.append(rec)

        infoQuantIP = {
            "ip": ip,
            "quantidade": quantidade,
            "recursos": primeiraParteRecurso,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
        }
        jsonIp.append(infoQuantIP)

    jsonIp = sorted(jsonIp, key=lambda x: x["quantidade"], reverse=True) # Esta ordenando os ips

    for info in jsonIp[:10]:
        print(f'Ip: {info["ip"]}\nquantidade: {info["quantidade"]}\ncidade: {info["city"]}\nregiao: {info["region"]}\npais: {info["country"]}')
        print(f"Quantidade dos recursos")
        contabilizandoRecursos(info["recursos"])
        print("-------------------------------------------------------")
# %%

print("Informacoes sobre o get 404")
mostrarInfo(GET404)
print("Informacoes sobre o post 404")
mostrarInfo(POST404)
print("Informacoes sobre o head 404")
mostrarInfo(HEAD404)
print("Informacoes sobre o put 404")
mostrarInfo(PUT404)
print("Informacoes sobre o patch 404")
mostrarInfo(PATCH404)
print("Informacoes sobre o connect 404")
mostrarInfo(CONNECT404)
#resultado = PATCH404.apply(separandoString, axis=1)
#print(resultado[12673])

# %%
print("INFORMACOES SOBRE O STATUS 429")
print("Informacoes sobre o get 429")
mostrarInfo(GET429)
print("Informacoes sobre o post 429")
mostrarInfo(POST429)

