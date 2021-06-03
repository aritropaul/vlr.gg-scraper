from fastapi import FastAPI, Request
from src.news import News
from src.matches import Matches
from src.team import Team
from src.player import Player
from src.events import Events
from src.streams import Streams

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

@app.get("/streams")
async def streams():
    return Streams.streams()

@app.get("/match/{id}")
async def match(id):
    return Matches.match(id)

@app.get("/team/{id}")
async def team(id):
    return Team.team(id)

@app.get("/player/{id}")
async def player(id):
    return Player.player(id)

@app.get("/events")
async def events():
    events = Events()
    return events.region("all")

@app.get("/events/{id}")
async def events(id):
    events = Events()
    return events.region(id)