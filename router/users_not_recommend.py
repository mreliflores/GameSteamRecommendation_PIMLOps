from fastapi import APIRouter, HTTPException
from schemas.users_not_recommend import UsersNotRecommend_
import pandas as pd

unr = APIRouter()

games = pd.read_csv('data/games.csv', lineterminator='\n')

reviews = pd.read_csv('data/sentiment_analysis.csv', lineterminator='\n')

recommend0 = reviews.recommend == 0
sentiment0 = reviews.sentiment == 0

def UsersNotRecommend(year):
  mask_year = reviews.year == year
  query = reviews[
      recommend0 & sentiment0 & mask_year
  ]
  query.reset_index(drop=True, inplace=True)
  query = query.groupby(
      by='id_game'
  ).agg(count=('sentiment', 'count')).sort_values(
      by='count', ascending=False
  )

  query = query.merge(games[['id_game', 'title']], on='id_game')

  print(query)

  worst_games = []

  for i, game in enumerate(query['title'].values):
    item = {f'Position {i+1}': game}
    worst_games.append(item)
    if i+1 == 3:
      break
  return worst_games


@unr.get("/{year}", response_model=list[UsersNotRecommend_])
async def get_not_Recomend(
  year: int
):
  """
  Get not recommend games. Suggested inputs from 2010 until 2015
  """
  if year not in reviews['year'].values:
    raise HTTPException(
      status_code=404,
      detail="Doesn't exists reviews in this year"
    )
  response = UsersNotRecommend(year)
  return response