from fastapi import APIRouter, HTTPException
from schemas.playtime_genre import PlayTimeGenre_
import pandas as pd

ptg = APIRouter()

games = pd.read_csv('data/games.csv', lineterminator='\n')

genres_dummies = pd.read_csv('data/genres.csv', lineterminator='\n')

playtime_per_game = pd.read_csv('data/playtimePerGame.csv', lineterminator='\n')


def PlayTimeGenre(genre):

  query = playtime_per_game.merge(
    games[['id_game', 'year']],
    on='id_game'
  ) #Merge with game df to get release year

  query = query.merge(
    genres_dummies,
    on='id_game'
  ) # Merge with genres_dummies df to enable the filtro by genre
  query.drop(
    columns=['id_game'],
    inplace=True
  ) #Drop the unnecessary id_game column
  
  query.reset_index(drop=True, inplace=True)

  query = query[
    query[genre]==1               #Filter by genre
  ].groupby(
    by='year',                    #Group by release year
    as_index=False
  ).agg(playtime_forever=(
    'playtime_forever', 'sum'     #Apply aggregation funcion to playtime
  )).sort_values(
    by='playtime_forever',        #Sort to get the most playtime
    ascending=False
  )
  
  query.reset_index(drop=True, inplace=True)

  response = {
    f"Release date with the most playtime for Genre {genre}" : int(query.loc[0].year)
  }

  return response




@ptg.get("/{genre}", response_model=PlayTimeGenre_)
async def get_more_playtime_genre(
  genre: str
):
  """
  Obtener obras
  """
  if genre not in genres_dummies.columns:
    raise HTTPException(
      status_code=404,
      detail=f"The genre {genre} doesn't exist."
    )
  response = PlayTimeGenre(genre)
  return response