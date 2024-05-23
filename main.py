from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

# Base url that connects us to the server where the movie info is located
url = "https://imdb8.p.rapidapi.com/auto-complete"

# These headers are used to authenticate your connection
headers = {
    "X-RapidAPI-Key": "432023f41emsh1ce2d46caac39f6p1fe6fejsn932e8404f419",
    "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_terms = request.form["search_terms"].split(",")
        movie_responses = []
        series_responses = []

        for term in search_terms:
            querystring = {"q": term.strip()}
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data = response.json()
            filtered_data = [movie for movie in data.get(
                "d", []) if movie.get("id", "").startswith("tt")]

            # Separate movies and TV series
            movies = [item for item in filtered_data if item.get(
                "qid") == "movie"]
            series = [item for item in filtered_data if item.get(
                "qid") == "tvSeries"]

            movie_responses.append(movies)
            series_responses.append(series)

        return render_template("index.html", movie_responses=movie_responses, series_responses=series_responses, search_terms=search_terms, enumerate=enumerate)

    return render_template("index.html", movie_responses=None, series_responses=None)


if __name__ == "__main__":
    app.run(debug=True)
