import requests
import secret

def AnilistData(name:str, media_type:str) -> dict:
    url = 'https://graphql.anilist.co'

    id_parameters = {
        'query': name,  # Media name --> String
        'format': media_type,  # Either ANIME or MANGA
        'page': 1,  # Amount of pages to retrieve data
        'perpage': 3  # Items per page
    }

    query = """\
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
                    format
                    duration
                    episodes
                    chapters
                }
            }
        }
    """
    # The duration part is purged during the FilterData() on interface.py
    response = requests.post(url, json={'query': query, 'variables': id_parameters})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        if isinstance(response, str):  # Check if entry_data is a string
            return {'error':'Desired content not found'}

        # Extract the JSON content from the response
        json_content = response.json()
        return json_content
    
    else:
        # Print the error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return {'error': f"Error: {response.status_code}, {response.text}"}

def MovieSearch(show_name:str) -> object:
    url = "https://api.themoviedb.org/3/search/movie?query={}&include_adult=true&page=1"

    headers = {
        "accept": "application/json",
         "Authorization": f"Bearer {secret.MovieTOKEN}"
    }
    # Format the URL with the provided information
    new_url = url.format(show_name.replace(" ", "%20"))

    response = requests.get(new_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        json_content = response.json()
        return json_content
    
    else:
        # Print the error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return {'error': f"Error: {response.status_code}, {response.text}"}

def MovieData(movie_id:int):
    url = "https://api.themoviedb.org/3/movie/{}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {secret.MovieTOKEN}"
    }

    new_url = url.format(movie_id)

    response = requests.get(new_url, headers=headers) 

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        json_content = response.json()
        return json_content
    
    else:
        # Print the error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return {'error': f"Error: {response.status_code}, {response.text}"}