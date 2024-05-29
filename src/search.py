import requests
import settings

# Base URLs and headers
ANILIST_URL = 'https://graphql.anilist.co'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.MovieTOKEN}"
}
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes?q={}'

def fetch_data(url, headers=None, payload=None):
    if payload:
        response = requests.post(url, json=payload, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {'error': f"Error: {response.status_code}, {response.text}"}

def AnilistData(name: str, media_type: str) -> dict:
    query = """
        query ($query: String, $format: MediaType, $page: Int, $perpage: Int) {
            Page (page: $page, perPage: $perpage) {
                media (search: $query, type: $format) {
                    title {
                        romaji
                        english
                    }
                    type
                    genres
                    countryOfOrigin
                    startDate {
                        year
                        month
                        day
                    }
                    duration
                    episodes
                    chapters
                }
            }
        }
    """
    variables = {
        'query': name,
        'format': media_type,
        'page': 1,
        'perpage': 3
    }
    return fetch_data(ANILIST_URL, payload={'query': query, 'variables': variables})

def MovieSearch(show_name: str) -> dict:
    url = f"{TMDB_BASE_URL}/search/movie?query={show_name.replace(' ', '%20')}&include_adult=true&page=1"
    return fetch_data(url, headers=TMDB_HEADERS)

def MovieData(movie_id: int) -> dict:
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    return fetch_data(url, headers=TMDB_HEADERS)

def TVShowSearch(show_name: str) -> dict:
    url = f"{TMDB_BASE_URL}/search/tv?query={show_name.replace(' ', '%20')}&include_adult=true&page=1"
    return fetch_data(url, headers=TMDB_HEADERS)

def TVShowData(tv_show_id: int) -> dict:
    url = f"{TMDB_BASE_URL}/tv/{tv_show_id}"
    return fetch_data(url, headers=TMDB_HEADERS)

def BookSearch(book_name: str) -> dict:
    url = GOOGLE_BOOKS_API_URL.format(book_name.replace(' ', '+'))
    return fetch_data(url)