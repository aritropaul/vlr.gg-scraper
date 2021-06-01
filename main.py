from fastapi import FastAPI, Request
from src.news import News
from src.matches import Matches
from src.team import Team
from src.player import Player

app = FastAPI()

@app.get("/")
async def health_check():
    return 'OK'

@app.get("/news")
async def news():
    return News.news()

@app.get("/upcoming")
async def matches():
    return Matches.upcoming_matches()

@app.get("/results")
async def matches():
    return Matches.recent_matches()

@app.get("/match/{id}")
async def match(id):
    return Matches.match(id)

@app.get("/team/{id}")
async def team(id):
    return Team.team(id)

@app.get("/player/{id}")
async def player(id):
    return Player.player(id)