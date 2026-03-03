import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Lendo o arquivo states.csv e atribuindo à variável states
states = pd.read_csv("./data/states.csv")

# Análise descritiva

# Criando lista contendo os nomes das variáveis relacionadas à qualidade de vida
cols = ["IDH", "Expectativa de vida", "PIB per capita", "Mortalidade infantil"]

# Imprimindo informações estatísticas das variáveis de qualidade de vida e da alfabetização, arredondando para 4 casas decimais
print(states[cols + ["Alfabetização"]].describe().round(4))

# Criando ranking de alfabetização em ordem decrescente
ranking = states.sort_values("Alfabetização", ascending=False)

# Definindo dimensões do gráfico
plt.figure(figsize=(9,6))

# Plotando gráfico de barras horizontais com estados no eixo Y e alfabetização como comprimento das barras 
plt.barh(ranking["Unidade federativa"], ranking["Alfabetização"])

# Definindo rótulo do eixo X e título do gráfico
plt.xlabel("Alfabetização")
plt.title("Ranking de Alfabetização por Estado")

# Invertendo eixo Y para posicionar o maior valor no topo
plt.gca().invert_yaxis()

# Ajustando layout para evitar sobreposição de elementos
plt.tight_layout()

# Exibindo o gráfico criado
plt.show()

# Correlação

# Criando objeto StandarScaler para padronizar as variáveis (z-score)
scaler = StandardScaler()

# Criando novas colunas que receberão os valores padronizados
states[["IDH_z", "Expectativa de vida_z", "PIB per capita_z", "Mortalidade infantil_z"]] = scaler.fit_transform(states[cols])

# Invertendo a mortalidade infantil para que os valores altos representem melhor qualidade de vida
states["Mortalidade infantil_z"] = -states["Mortalidade infantil_z"]

# Criando lista contendo os nomes das variáveis relacionadas à qualidade de vida ajustadas
cols_z = ["IDH_z", "Expectativa de vida_z", "PIB per capita_z", "Mortalidade infantil_z"]

# Criando índice qualidade de vida (média das variáveis padronizadas)
states["Qualidade de vida"] = states[cols_z].mean(axis=1)

# Calculando a correlação entre alfabetização e qualidade de vida
correlation = states["Alfabetização"].corr(states["Qualidade de vida"])

# Imprimindo valor da correlação entre alfabetização e qualidade de vida, arredondando para 2 casas decimais
print("Correlação entre alfabetização e qualidade de vida:", round(correlation, 2))

# Definindo dimensões do gráfico
plt.figure(figsize=(9,6))

# Plotando gráfico de dispersão com alfabetização no eixo X e qualidade de vida no eixo Y 
plt.scatter(states["Alfabetização"], states["Qualidade de vida"])

# Definindo rótulos dos eixos e título do gráfico
plt.xlabel("Alfabetização")
plt.ylabel("Qualidade de vida")
plt.title("Alfabetização x Qualidade de Vida nos Estados Brasileiros")

# Exibindo o gráfico criado
plt.show()

# Dados por região

# Calculando média regional de alfabetização e qualidade de vida
regional_means = states.groupby("Região", as_index=False)[["Alfabetização", "Qualidade de vida"]].mean().sort_values("Alfabetização", ascending=False).reset_index(drop=True)

# Padronizando valor de alfabetização (z-score)
regional_means["Alfabetização_z"] = scaler.fit_transform(regional_means[["Alfabetização"]])

# Imprimindo na tela a média regional de alfabetização e qualidade de vida
print(regional_means)

# Definindo dimensões do gráfico
plt.figure(figsize=(9,6))

# Plotando gráfico de barras verticais com regiões no eixo X e alfabetização no eixo Y
plt.bar(regional_means["Região"], regional_means["Alfabetização_z"])

# Definindo rótulo do eixo Y e título do gráfico
plt.ylabel("Alfabetização (padronizada)")
plt.title("Média de Alfabetização por Região")

# Ajustando layout para evitar sobreposição de elementos
plt.tight_layout()

# Exibindo o gráfico criado
plt.show()

# Definindo dimensões do gráfico
plt.figure(figsize=(9,6))

# Plotando gráfico de barras verticais com regições no eixo X e alfabetização no eixo Y
plt.bar(regional_means["Região"], regional_means["Qualidade de vida"])

# Definindo rótulo do eixo Y e título do gráfico
plt.ylabel("Qualidade de vida")
plt.title("Média de Qualidade de Vida por Região")

# Ajustando layout para evitar sobreposição de elementos
plt.tight_layout()

# Exibindo o gráfico criado
plt.show()
