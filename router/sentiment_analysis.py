from fastapi import APIRouter, HTTPException
from schemas.sentiment_analysis import SentimentAnalysis
import pandas as pd

sa = APIRouter()

games = pd.read_csv('data/games.csv', lineterminator='\n')

sentiment_analysis_table = pd.read_csv('data/sentiment_analysis.csv', lineterminator='\n')

defaul_keys = ['negative', 'neutral', 'positive']

def sentiment_name(value):
  if value==0:
    return 'negative'
  elif value==1:
    return 'neutral'
  elif value==2:
    return 'positive'

sentiment_analysis_table['sentiment'] = sentiment_analysis_table['sentiment'].apply(sentiment_name)

def sentiment_analysis(year):
  toFunctSA = games[
    ['id_game', 'year']
  ].merge(
    sentiment_analysis_table[
      ['id_game', 'sentiment']
    ],
    on='id_game'
  )

  response = toFunctSA.groupby(
    by=['year', 'sentiment']
  ).agg(
    count=('id_game', 'count')
  ).loc[year].to_dict()['count']

  for i in range(0, 3):
    
    if defaul_keys[i] not in response.keys():
      response[defaul_keys[i]] = 0

  return response




@sa.get("/{year}", response_model=SentimentAnalysis)
async def get_sentiment(
  year: int
):
  """
  Obtener obras
  """
  if (year not in games['year'].values):
    raise HTTPException(
      status_code=404,
      detail="This year doesn't exist in release year or there is not review for games with this release year"
    )
  response = sentiment_analysis(year)
  return response