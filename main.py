import uvicorn
from bs4 import BeautifulSoup
import httpx
import os
from typing import Optional
from fastapi import FastAPI, Depends
from cachetools import TTLCache
app = FastAPI()

cache = TTLCache(maxsize=100, ttl=360)


async def fetch_html(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response


def checkTopic(topic: str, array: list[dict[str]]) -> list[dict[str]]:
    result = []

    for dictionary in array:
        for key, value in dictionary.items():
            if isinstance(value, str) and topic.lower() in value.lower():
                result.append(dictionary)
                break
    if result:
        cache[topic.lower()] = result
    return result


async def gameRant(topic: Optional[str]):
    url = "https://gamerant.com/gaming/"
    if topic and topic.lower() in cache:
        return cache[topic.lower()]
    if url in cache:
        if topic:

            checkTopic(topic, cache[url])
        else:
            return cache[url]
    html_content = await fetch_html(url)
    soup = BeautifulSoup(html_content.content, "html.parser")
    contents = soup.find_all('div', class_="w-display-card-content")
    news = []
    for content in contents:
        doc = {}
        title = content.find(
            'h5', class_='display-card-title').text.strip()

        if topic and not (topic.lower() in title.lower()):
            continue
        else:
            doc["title"] = title
            doc["description"] = content.find(
                'p', class_='display-card-excerpt').text.strip()
            doc["updated"] = content.find(
                'time', class_='display-card-date').text.strip()
            doc["source"] = url

        news.append(doc)
    if not topic:
        cache[url] = news
    else:
        if news:
            cache[topic] = news
    return news


async def pcgamer(topic: Optional[str]):

    url = "https://www.pcgamer.com/news/"

    if topic and topic.lower() in cache:

        return cache[topic.lower()]
    if url in cache:
        if topic:
            checkTopic(topic, cache[url])
        else:
            return cache[url]
    html_content = await fetch_html(url)
    soup = BeautifulSoup(html_content.content, "html.parser")
    contents = soup.find_all('div', class_='content')
    news = []
    for content in contents:
        doc = {}
        title = content.find('h3', class_='article-name').text.strip()
        if topic and (topic.lower() not in title.lower()):
            continue
        else:
            doc["title"] = title
            doc["description"] = content.find(
                'p', class_='synopsis').text.strip()
            doc["updated"] = content.find(
                'time', class_='no-wrap relative-date date-with-prefix').text.strip()
            doc["source"] = url

        news.append(doc)
    if not topic:
        cache[url] = news
    else:
        if news:
            cache[topic] = news
    return news


@app.get("/")
async def gather_news(topic: Optional[str] = None):
    gameR = await gameRant(topic)
    pcgam = await pcgamer(topic)
    if not gameR:
        return pcgam
    if not pcgam:
        return gameR
    else:
        return gameR+pcgam

if __name__ == '__main__':
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
