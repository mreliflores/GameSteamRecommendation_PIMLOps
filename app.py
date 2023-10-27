from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #to fetch from front debug
from router.sentiment_analysis import sa
from router.users_not_recommend import unr
from router.users_recommend import ur
from router.playtime_genre import ptg
from router.user_genre import ufg


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
  sa,
  prefix="/sentiment_analysis",
  tags=["sentiment_analysis"]
)

app.include_router(
  unr,
  prefix="/users_not_recommend",
  tags=["users_not_recommend"]
)

app.include_router(
  ur,
  prefix="/users_recommend",
  tags=["users_recommend"]
)

app.include_router(
  ptg,
  prefix="/playtime_genre",
  tags=["playtime_genre"]
)

app.include_router(
  ufg,
  prefix="/user_for_genre",
  tags=["user_for_genre"]
)