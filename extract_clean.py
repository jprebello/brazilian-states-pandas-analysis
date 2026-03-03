import pandas as pd
import requests
from io import StringIO

# URL da página da Wikipedia contendo a tabela das Unidades federativas do Brasil
url = "https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil"

# Fazendo a requisição com header para evitar bloqueios da página
response = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})

# Lendo todas as tabelas HTML da página
dfs = pd.read_html(StringIO(response.text))

# Verificando as primeiras linhas de cada tabela encontrada para identificar qual contém os dados das Unidades federativas
for i, df in enumerate(dfs):
    print("\nTabela:", i)
    print(df.head().to_string())

# Criando um DataFrame para tabela de Unidades federativas
states = dfs[1]

# Imprimindo as colunas do DataFrame
print(states.columns)

# Removendo colunas desnecessárias para análise
states = states.drop(columns=["Bandeira", "Abreviação", "Sede de governo", "Área (km²)", "População (Censo 2022)", "Densidade (2005)", "PIB (2015)", "(% total) (2015)"])

# Imprimindo a tipagem de cada coluna restante
print(states.dtypes)

# Renomeando as colunas
states = states.rename(columns={"PIB per capita (R$) (2015)": "PIB per capita",
                                "IDH (2010)": "IDH",
                                "Alfabetização (2016)": "Alfabetização",
                                "Mortalidade infantil (2016)": "Mortalidade infantil",
                                "Expectativa de vida (2016)": "Expectativa de vida"})

# Criando função para converter valores em float
def to_float(x):
    x = str(x)
    x = x.replace(",", ".").strip().replace("%", "").replace("‰", "").replace(" anos", "").replace(" ","").replace("\xa0","")
    return float(x)

# Aplicando a função to_float para todas as linhas de cada coluna do DataFrame
states["PIB per capita"] = states["PIB per capita"].apply(to_float)
states["IDH"] = states["IDH"].apply(to_float)
states["Alfabetização"] = states["Alfabetização"].apply(to_float)
states["Mortalidade infantil"] = states["Mortalidade infantil"].apply(to_float)
states["Expectativa de vida"] = states["Expectativa de vida"].apply(to_float)

# Criando função que devolve a região de acordo com a Unidade federativa
def to_region(uf):
    if uf in ["Distrito Federal", "Goiás", "Mato Grosso", "Mato Grosso do Sul"]:
        return "Centro-Oeste"
    
    elif uf in ["Acre", "Amapá", "Amazonas", "Pará", "Rondônia", "Roraima", "Tocantins"]:
        return "Norte"
    
    elif uf in ["Alagoas", "Bahia", "Ceará", "Maranhão", "Paraíba", 
                "Pernambuco", "Piauí", "Rio Grande do Norte", "Sergipe"]:
        return "Nordeste"
    
    elif uf in ["Espírito Santo", "Minas Gerais", "Rio de Janeiro", "São Paulo"]:
        return "Sudeste"
    
    elif uf in ["Paraná", "Rio Grande do Sul", "Santa Catarina"]:
        return "Sul"
    
    else:
        return "UF inválida"

# Aplicando a função to_region e padronizando o valor de algumas variáveis
states["Região"] = states["Unidade federativa"].apply(to_region)
states["IDH"] = states["IDH"] / 1000
states["Alfabetização"] = states["Alfabetização"] / 100
states["Mortalidade infantil"] = states["Mortalidade infantil"] / 1000

# Exportando o DataFrame states em um arquivo csv (sem salvar o índice)
states.to_csv("./data/states.csv", index=False)
