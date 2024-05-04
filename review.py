import requests
from pydantic import BaseModel, Field

# Define the model for movie query
class MovieQuery(BaseModel):
    movie_name: str = Field(description="The name of the movie to query.")

# Function to query movie details
def query_movie(movie_name):
    api_key = 'YOUR_API_KEY'  # Replace 'YOUR_API_KEY' with your actual API key
    url = "https://movie-database-imdb.p.rapidapi.com/movie/"
    querystring = {"name": movie_name}
    headers = {
        "X-RapidAPI-Key": "e3a26d3d91msh1df956f0cff2a43p1c4efbjsn35d8a93e0c81",
        "X-RapidAPI-Host": "movie-database-imdb.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            movie_data = response.json()
            message = f"Title: {movie_data.get('name')}\n"
            message += f"Release Date: {movie_data.get('datePublished')}\n"
            message += f"Rating: {movie_data.get('rating').get('ratingValue')}\n"
            message += f"Genre: {', '.join(movie_data.get('genre'))}\n"
            message += "Actors:\n"
            for actor in movie_data.get('actor'):
                message += f"- {actor.get('name')}\n"
            message += "Director:\n"
            for director in movie_data.get('director'):
                message += f"- {director.get('name')}\n"
            message += f"Description: {movie_data.get('description')}"
        else:
            message = "Failed to fetch movie information."
    except Exception as e:
        message = f"Error: {str(e)}"
    return message

# Define the model for movie search
class MovieSearch(BaseModel):
    movie_name: str

# Function to search for movie torrents
def search_movie(movie_name):
    rapidapi_key = 'e3a26d3d91msh1df956f0cff2a43p1c4efbjsn35d8a93e0c81'
    url = "https://movie-tv-music-search-and-download.p.rapidapi.com/search"
    querystring = {"keywords": movie_name, "quantity": "5", "page": "1"}
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "movie-tv-music-search-and-download.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    results = []
    if 'result' in data:
        for item in data['result']:
            result = {
                'title': item.get('title', 'N/A'),
                'size': item.get('size', 'N/A'),
                'torrent': item.get('torrent', 'N/A')
            }
            results.append(result)
    return results

# Ask for movie name
movie_name = input("Enter the name of the movie: ")

# Query movie details
movie_review = query_movie(movie_name)
print(movie_review)

# Ask if user wants torrent links
torrent_choice = input("Do you want torrent links for this movie? (yes/no): ")

# If user wants torrent links, search for them
if torrent_choice.lower() == "yes":
    torrent_results = search_movie(movie_name)
    if torrent_results:
        print("\nTorrent Links:")
        for result in torrent_results:
            print(f"Title: {result['title']}\nSize: {result['size']}\nTorrent: {result['torrent']}\n")
    else:
        print("No torrent links found for the given movie.")
