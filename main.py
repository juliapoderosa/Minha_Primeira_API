from fastapi import FastAPI
import pandas as pd
import uvicorn 
import json
from fastapi import FastAPI
import pandas as pd

# Criar a aplicação
app = FastAPI()

# Carregar os dados do CSV
df = pd.read_csv('world_imdb_movies_top_movies_per_year (1).csv')  # ajuste o nome do arquivo para o que você realmente tem
filmes = df.to_dict(orient="records")

@app.get("/")
def home():
    """Endpoint básico que retorna informações sobre a API"""
    return {
        "projeto": "API de Filmes",
        "autor": "Julia Ribeiro",
        "descricao": "API para consultar informações sobre filmes",
        "total_registros": len(filmes)
    }

@app.get("/filmes")
def listar_todos():
    """Retorna todos os filmes"""
    return filmes

@app.get("/filmes/{id}")
def buscar_filme(id: int):
    """Busca um filme pelo ID"""
    for filme in filmes:
        if filme["id"] == id:
            return filme
    return {"erro": "Filme não encontrado"}
from fastapi import FastAPI
import pandas as pd
import basedosdados as bd

app = FastAPI()

# seu billing_id do Google Cloud
BILLING_ID = "meu_projeto_no_gcp"  # substitua pelo seu ID real

@app.get("/buscar")
def buscar_com_filtros(nome: str = None, categoria: str = None, limite: int = 10):
    """
    Endpoint INTERMEDIÁRIO: Busca com parâmetros de query no BigQuery
    """

    # Query básica
    query = """
      SELECT
        id,
        original_title,
        genres,
        release_date
      FROM `basedosdados.world_imdb_movies.top_movies_per_year`
      LIMIT {limite}
    """.format(limite=limite)

    # Lê os dados do BigQuery
    df = bd.read_sql(query=query, billing_project_id=BILLING_ID)

    # Converte em dicionários
    resultados = df.to_dict(orient="records")

    # Aplicar filtros opcionais
    if nome:
        resultados = [r for r in resultados if nome.lower() in r["original_title"].lower()]
    if categoria:
        resultados = [r for r in resultados if categoria.lower() in (r["genres"] or "").lower()]

    return {
        "filtros": {"nome": nome, "categoria": categoria, "limite": limite},
        "resultados": resultados,
        "total": len(resultados)
    }



