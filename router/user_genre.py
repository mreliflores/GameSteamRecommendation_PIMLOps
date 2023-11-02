from fastapi import APIRouter, HTTPException
from schemas.user_genre import UserForGenre_
import pandas as pd

ufg = APIRouter()

playtime_per_user = pd.read_csv('data/playTimePerUser.csv', lineterminator='\n')

genres_dummies = pd.read_csv('data/genres.csv', lineterminator='\n')

def UserForGenre(genre):
  query = playtime_per_user[playtime_per_user[genre]==1].groupby(by='user_id', as_index=False).agg(playtime_forever=('playtime_forever', 'sum')).sort_values(by='playtime_forever', ascending=False)

  query.reset_index(
    drop=True,
    inplace=True
  )
  bestUser = query.loc[0]['user_id']

  years = playtime_per_user[
    playtime_per_user['user_id'] == bestUser
  ][[
    'user_id', 'year', 'playtime_forever'
  ]]

  years = years.groupby(
    by=['user_id', 'year'],
    as_index=False
  ).agg(playtime_forever=(
    'playtime_forever', 'sum'
  ))

  playtimeList_per_year = []

  for year, playtime in zip(years['year'], years['playtime_forever']):
    dictionarie = {
      'year': year,
      'hours': int(playtime)
    }

    playtimeList_per_year.append(
      dictionarie
    )

  response = {
    f"User with the most playtime for Genre {genre}" : bestUser,
    "Playtime": playtimeList_per_year
  }

  return response

@ufg.get("/{genre}", response_model=UserForGenre_|None)
async def get_user_more_playtime_genre(
  genre: str
):
  """
  Get the user with the most playtime by genre. Suggested input
  [
  action,
  adventure,
  indie
  ]
  """
  if genre not in genres_dummies.columns:
    raise HTTPException(
      status_code=404,
      detail=f"The genre {genre} doesn't exist."
    )
  response = UserForGenre(genre)
  return response