from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn
from typing import Optional
try:
    dados = pd.read_csv(r"C:\Users\Dell\Downloads\archive (2)\world_imdb_movies_top_movies_per_year (2).csv")

    movies  = dados.to_dict("records")
    print(f"✅ Dados carregados: {len(movies)} itens")
except FileNotFoundError:
    print("❌ Arquivo world_imdb_movies_top_movies_per_year (2).csv não encontrado!")
    movies  = []
    #Criar app FastAPI
app = FastAPI(
    title=" API do IMDB",
    description="API para consultar filmes do IMDB",
    version="1.0.0"
)
@app.get("/")
def home():
    """
    Endpoint básico que retorna informações sobre a API
    """
    return {
        "projeto": "API do IMDB",
        "autor": "Seu Nome Aqui",
        "descricao": "API para servir dados do IMDB",
        "total_registros": len(movies),
        "categorias": list(set([item["categoria"] for item in movies])),
        "documentacao": "/docs"
    }
@app.get("/dados")
def listar_todos():
    """
    ENDPOINT BÁSICO: Retorna TODOS os itens do cardápio
    """
    if not cardapio:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
    
    return {
        "total": len(movies),
        "dados": movies
    }

@app.get("/dados/{item_id}")
def buscar_por_id(item_id: int):
    """
    ENDPOINT INTERMEDIÁRIO: Busca um item específico pelo ID
    Exemplo: /dados/5
    """
    item = next((item for item in movies if item["id"] == item_id), None)
    
    if not item:
        raise HTTPException(status_code=404, detail=f"Item com ID {item_id} não encontrado")
    
    return {
        "encontrado": True,
        "item": item

    }
@app.get("/categoria/{categoria}")
def buscar_por_categoria(categoria: str):
    """
    ENDPOINT INTERMEDIÁRIO ALTERNATIVO: Filtra itens por categoria de filmes 
    """
    itens_categoria = [item for item in movies if item["categoria"].lower() == categoria.lower()]
    
    if not itens_categoria:
        categorias_disponiveis = list(set([item["categoria"] for item in movies]))
        raise HTTPException(
            status_code=404, 
            detail=f"Categoria '{categoria}' não encontrada. Categorias disponíveis: {categorias_disponiveis}"
        )
    
    return {
        "categoria": categoria,
        "total": len(itens_categoria),
        "itens": itens_categoria
    }@app.get("/buscar")
def buscar_com_filtros(nome: Optional[str] = None, categoria: Optional[str] = None, preco_max: Optional[float] = None, limite: int = 10):
    """
    ENDPOINT INTERMEDIÁRIO ALTERNATIVO: Busca com múltiplos filtros
    Exemplo: /buscar?nome=pizza&preco_max=30&limite=5
    Exemplo: /buscar?categoria=lanches
    """
    resultados = movies.copy()
    
    # Filtrar por nome (busca parcial)
    if nome:
        resultados = [item for item in resultados if nome.lower() in item["nome"].lower()]
    
    # Filtrar por categoria
    if categoria:
        resultados = [item for item in resultados if item["categoria"].lower() == categoria.lower()]

    # Filtrar por preço máximo
    if preco_max is not None:
        resultados = [item for item in resultados if item["preco"] <= preco_max]

    # Limitar resultados
    resultados = resultados[:limite]

    return {
        "total": len(resultados),
        "dados": resultados
    }




