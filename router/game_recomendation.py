from fastapi import APIRouter, HTTPException
from numpy.linalg import norm
from numpy import dot
import pandas as pd

gr = APIRouter()

games = pd.read_csv('data/games.csv', lineterminator='\n', index_col='id_game')

features = pd.read_csv('data\MLFeatures.csv', lineterminator='\n', index_col='id_game')

def game_recommendation(id_game, df_feat):

  return None

def normalize(df):
  return df.apply(
    lambda x: x.values/norm(x.values),
    axis=1,
    result_type='expand'
  )

def cosine_simmilarity(v1, v2):
  return dot(v1, v2) / ( norm(v1) * norm(v2) )


@gr.get("/{id_game}")
async def get_game_recommendation(
  id_game: int
):
  """
  Recommendation system using cosine simmilarity
  """
  if id_game not in games.index:
    raise HTTPException(
      status_code=404,
      detail=f"The game doesn't exist."
    )
  response = game_recommendation(id_game)
  return response