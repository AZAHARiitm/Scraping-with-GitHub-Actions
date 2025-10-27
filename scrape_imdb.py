import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.imdb.com/search/title/?user_rating=7.0,8.0&count=25"
HEADERS = {"Accept-Language": "en-US,en;q=0.5", "User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

movies = []
for idx, item in enumerate(soup.select(".lister-item.mode-advanced"), 1):
    header = item.select_one("h3.lister-item-header a")
    title_text = f"{idx}. {header.text.strip()}"
    link = header["href"]
    movie_id = link.split("/")[2]  # Extract ttXXXXXX
    year_tag = item.select_one(".lister-item-year")
    year_text = year_tag.text.strip() if year_tag else ""
    rating_tag = item.select_one(".ratings-imdb-rating strong")
    rating_text = rating_tag.text.strip() if rating_tag else ""

    movies.append({
        "id": movie_id,
        "title": title_text,
        "year": year_text,
        "rating": rating_text
    })

print(json.dumps(movies, indent=2))
