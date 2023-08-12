from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_movie_data():
    url = 'https://www.imdb.com/list/ls029559286/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    movie_list = []
    movies = soup.find_all('div', class_='lister-item-content')

    for movie in movies:
        title = movie.find('h3').find('a').text
        year = movie.find('span', class_='lister-item-year').text.strip('()')
        rating = movie.find('div', class_='ipl-rating-star small').find('span', class_='ipl-rating-star__rating').text.strip()

        movie_list.append({'title': title, 'year': year, 'rating': rating})

    movie_list.sort(key=lambda movie: int(movie['year']))
    return movie_list

@app.route('/')
def index():
    movies = get_movie_data()
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
