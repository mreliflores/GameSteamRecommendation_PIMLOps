from fastapi import APIRouter, HTTPException
from numpy.linalg import norm
from numpy import dot
import pandas as pd

gr = APIRouter()

games = pd.read_csv('data/games.csv', lineterminator='\n', index_col='id_game')

features = pd.read_csv('data/MLFeatures.csv', lineterminator='\n', index_col='id_game')

def game_recommendation(id_game, df_feat: pd.DataFrame):
  df_feat = normalize(df_feat) #df_feat normalized
  inputVec = df_feat.loc[id_game].values #gets values of the book_id inputed
  df_feat['sim']= df_feat.apply(
    lambda x: cosine_simmilarity(
      inputVec,
      x.values
    ),
    axis=1
  ) #dot product calculated

  simmilarity = df_feat['sim'].sort_values(
    ascending=False
  ).drop(id_game) #get only cosine simmilarity computed and drop the game inputed

  df_final = simmilarity.nlargest(
    20
  )  #get 20 games to recommend

  recommended_games = games.loc[
    df_final.index
  ]['title']  #Get the name of the games to recommend
  return recommended_games.sample(n=5)   #From 20 games I randomly take 5 games to recommend

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
  [
    10,
    20,
    30,
    40,
    50,
    346330,
    373330,
    388490,
    521570,
    519140
  ]

  You can input any id_game showed above
  """
  if id_game not in games.index:
    raise HTTPException(
      status_code=404,
      detail=f"The game doesn't exist."
    )
  response = game_recommendation(id_game, features)
  return response