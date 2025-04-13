import wikipedia
import requests
from bs4 import BeautifulSoup

# === KEYS ===
NEWS_API_KEY = "YOUR_NEWS_API"
WEATHER_API_KEY = "YOUR_WEATHER_API"

# ----------- Wikipedia Search -----------
def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"[Wikipedia]\n{summary}"
    except Exception:
        return "[Wikipedia] No results found."


# ----------- DuckDuckGo Web Search -----------
def search_web(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all('a', class_='result__a', limit=3)
        results = [f"{i + 1}. {link.text}\n{link['href']}" for i, link in enumerate(links)]
        return "[Web Search Results]\n" + "\n\n".join(results) if results else "[Web] No results found."
    except Exception:
        return "[Web] Error fetching results."


# ----------- NewsAPI Search -----------
def get_latest_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&language=en&pageSize=3"
    try:
        res = requests.get(url)
        data = res.json()

        if data.get("status") != "ok" or not data.get("articles"):
            return "[News] No articles found."

        news_output = "[Latest News]\n"
        for article in data["articles"]:
            title = article["title"]
            source = article["source"]["name"]
            url = article["url"]
            news_output += f"- {title} ({source})\n{url}\n\n"
        return news_output.strip()
    except Exception:
        return "[News] Error fetching data."


# ----------- Weather Search (OpenWeatherMap) -----------
def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return "[Weather] Location not found."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"[Weather]\n{city.title()}: {temp}°C, {desc.capitalize()}"
    except Exception:
        return "[Weather] Error fetching data."


# ----------- Main Answer Engine -----------
def answer_query(query):
    query_lower = query.lower()

    if "weather" in query_lower:
        city = query_lower.split("in")[-1].strip() if "in" in query_lower else "your location"
        return get_weather(city)

    elif "news" in query_lower or "latest" in query_lower:
        topic = query_lower.replace("latest news about", "").replace("latest news", "").strip()
        return get_latest_news(topic or "technology")

    elif "wiki" in query_lower or "who is" in query_lower or "what is" in query_lower:
        return search_wikipedia(query)

    else:
        return search_web(query)


# ----------- Chat Loop -----------
if __name__ == "__main__":
    print("📡 InfoSeeker AI - Powered by Web, Wikipedia, News, and Weather")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Ask InfoSeeker 🤖: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print("\n" + answer_query(user_input) + "\n")

