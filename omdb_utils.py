from urllib.parse import quote
import requests

def get_movie_details(title, api_key):
    encoded_title = quote(title)  # safely encode the movie title
    url = f"http://www.omdbapi.com/?t={encoded_title}&plot=full&apikey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        res = response.json()

        if res.get("Response") == "True":
            plot = res.get("Plot", "Plot not available")
            poster = res.get("Poster", "https://via.placeholder.com/150")
            return plot, poster
        else:
            return "Plot not available", "https://via.placeholder.com/150"

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return "Plot not available", "https://via.placeholder.com/150"
    except ValueError:
        print("Invalid JSON received")
        return "Plot not available", "https://via.placeholder.com/150"
