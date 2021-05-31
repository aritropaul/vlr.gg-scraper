from fastapi import FastAPI, Request
import src.news
import src.matches
import os

app = FastAPI()

@app.get("/")
async def health_check():
    return 'OK'

@app.get("/news")
async def news():
    return src.news.news()

@app.get("/news/{id}")
async def news(id):
    return src.news.article(id)

@app.get("/upcoming")
async def matches():
    return src.matches.upcoming_matches()

@app.get("/results")
async def matches():
    return src.matches.recent_matches()

@app.get("/match/{id}")
async def match(id):
    return src.matches.match(id)