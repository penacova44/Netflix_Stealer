import requests
from bs4 import BeautifulSoup
import libtorrent as lt
import multiprocessing

def get_netflix_shows():
    movies = []
    # Set the API endpoint and your API key
    endpoint = "https://imdb-api.com/Movies"
    api_key = "YOUR_API_KEY"

    # Set the parameters for the API request
    params = {
        "subscription": "netflix",  # Search for Netflix shows
        "language": "en-US",  # Search for English-language shows
        "sort": "rating",  # Sort the results by rating
        "limit": "1000",  # Return a maximum of 100 results
    }

    # Make the API request
    response = requests.get(endpoint, params=params, headers={
        "x-api-key": api_key
    })

    # Parse the JSON response
    data = response.json()

    # Print the titles of the shows
    for show in data["items"]:
        movies.append(show["title"])
    return movies

def get_magnet(movie_name):
    url = f'https://kickasstorrents.to/usearch/{movie_name}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find(class_='cellMainLink')
    movie_sub_url = link.get("href")
    url_movie = f'https://kickasstorrents.to/{movie_sub_url}'
    response = requests.get(url_movie)
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find(title="Magnet link")
    return str(link.get('href'))

def torrent_start(magnet_link):
    # Create a session object
    session = lt.session()

    # Set the session settings
    session.listen_on(6881, 6891)

    # Create an add_torrent_params object
    params = lt.add_torrent_params()

    # Set the magnet link
    params.url = magnet_link

    # Add the torrent
    handle = session.add_torrent(params)

    # Wait for the download to complete
    while (not handle.is_seed()):
        print(f"Progress: {handle.status().progress * 100:.2f}%")
        time.sleep(1)

    print("Download complete!")

def main():
    
    for i in get_netflix_shows:
        p = multiprocessing.Process(target=start_torrent, args=(get_magnet(i),))
        p.start()


if __name__ == '__main__':
    main()