import requests
from bs4 import BeautifulSoup

def get_watchlist(username):

    _domain = "https://letterboxd.com/"
    url = _domain + username + "/watchlist/"
    watchlist = []

    while True:

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch watchlist for {username}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
     
        # scrape all the movies in users watchlist
    #TODO add the release year
        for film in soup.find_all('div', class_='film-poster'):
            title_tag = film.find('img', class_='image')
            title = title_tag['alt']
            watchlist.append(title)

        # check if there is another page for users watchlist
        next_button = soup.find('a', class_='next')
        if next_button is None:
            break
        else:
            url = _domain + next_button['href']
    
    print(f'Analysed {username}\'s watchlist')
    return watchlist

def get_common_movies(usernames):
    if not usernames:
        return []
    
    watchlists = []
    
    for username in usernames:
        watchlist = get_watchlist(username)
        if watchlist:
            watchlists.append(set(watchlist))
    
    if not watchlists:
        return []
    
    # find common movies in all watchlists
    common_watchlist_movies = set.intersection(*watchlists)
    return common_watchlist_movies

if __name__ == "__main__":
    usernames = input("Enter usernames seperated by spaces: ").split()
    common_movies = get_common_movies(usernames)
    
    if common_movies:
        print("Common movies in watchlists:")
        for movie in common_movies:
            print(movie)
    else:
        print("No common movies found :(")
