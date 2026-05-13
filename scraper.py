import json
import httpx
from bs4 import BeautifulSoup
from datetime import datetime

SOURCE_URL = "http://www.jiangmen.gov.cn/bmpd/jmszfhcxjsj/index.html"
DATA_FILE = "data/site_data.json"


async def fetch_page():
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(SOURCE_URL)
        resp.encoding = "utf-8"
        return resp.text


def parse_banners(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    banners = []
    carousel = soup.select_one("#tpxw")
    if not carousel:
        return banners
    for item in carousel.select(".item"):
        a_tag = item.find("a")
        img_tag = item.find("img")
        if a_tag and img_tag:
            banners.append({
                "title": img_tag.get("title", "").strip(),
                "image_url": img_tag.get("src", "").strip(),
                "link": a_tag.get("href", "").strip(),
            })
    return banners


def parse_news_list(soup: BeautifulSoup, ul_id: str) -> list[dict]:
    ul = soup.select_one(f"#{ul_id}")
    news = []
    if not ul:
        return news
    for li in ul.select("li"):
        a_tag = li.find("a")
        span = li.find("span")
        if a_tag:
            news.append({
                "title": a_tag.get("title", a_tag.get_text(strip=True)),
                "link": a_tag.get("href", ""),
                "date": span.get_text(strip=True) if span else "",
            })
    return news


def parse_news(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    return {
        "work_news": parse_news_list(soup, "con_gzdt_1"),
        "notices": parse_news_list(soup, "con_gzdt_2"),
        "gov_info": parse_news_list(soup, "con_gzdt_3"),
    }


async def scrape_all() -> dict:
    html = await fetch_page()
    banners = parse_banners(html)
    news = parse_news(html)
    return {
        "banners": banners,
        "news": news,
        "updated_at": datetime.now().isoformat(),
    }


def load_data() -> dict:
    import os
    if not os.path.exists(DATA_FILE):
        return {"banners": [], "news": {"work_news": [], "notices": [], "gov_info": []}, "updated_at": None}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict):
    import os
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
