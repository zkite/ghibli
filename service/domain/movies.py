def get_movies(films, people):
    movies = []
    for f in films:
        movie = dict(film=f["title"], people=[])
        for p in people:
            if any(f["id"] in pf for pf in p["films"]):
                movie["people"].append(p["name"])
        movies.append(movie)
    return movies
