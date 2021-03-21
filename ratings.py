from movielens_analysis import CsvParser
from collections import Counter, defaultdict
from datetime import datetime
from movies import Movies as MoviesBase


def mean(values):
    if len(values) == 0:
        return float('nan')
    return sum(values) / len(values)


def median(values):
    if len(values) == 0:
        return float('nan')
    items = sorted(values)
    if len(items) % 2 == 1:
        return items[len(items)//2]
    return (items[len(items)//2-1] + items[len(items)//2]) / 2


def var(values):
    if not len(values):
        return float('nan')
    mean_value = mean(values)
    squared_diff = [(value - mean_value) ** 2 for value in values]
    return sum(squared_diff) / len(squared_diff)


class Ratings(CsvParser):
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file, path_to_movies_file):
        """
        Put here any fields that you think you will need.
        """
        super().__init__(path_to_the_file)
        self.filename_movies = path_to_movies_file

    def get_users(self):
        return Ratings.Users(self, self.filename_movies)

    def get_movies(self):
        return Ratings.Movies(self, self.filename_movies)

    def is_valid_file(self):
        return set(self.columns) == set('userId,movieId,rating,timestamp'.split(','))

    def read_csv(self):
        for film_info in super(Ratings, self).read_csv():
            if not self.is_valid_file():
                raise TypeError
            yield film_info

    class Movies(MoviesBase):
        def __init__(self, rating, movies_filename):
            super().__init__(movies_filename)
            self.rating = rating
            self.movies_id2name = {}

        def init_mapping_movies(self):
            for film_info in self.read_csv():
                self.movies_id2name[film_info['movieId']] = film_info['title']

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            ratings_by_year = Counter()
            for film_info in self.rating.read_csv():
                ratings_by_year[datetime.fromtimestamp(int(film_info['timestamp'])).year] += 1
            return dict(ratings_by_year.most_common()[::-1])
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            ratings_distribution = Counter()
            for film_info in self.rating.read_csv():
                ratings_distribution[float(film_info['rating'])] += 1
            return dict(ratings_distribution.most_common()[::-1])

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            self.init_mapping_movies()
            if n == -1:
                n = len(self.movies_id2name)
            top_movies = Counter()
            for film_info in self.rating.read_csv():
                top_movies[self.movies_id2name[film_info['movieId']]] += 1
            return dict(top_movies.most_common()[:n])

        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            assert metric in ('average', 'median')
            if n == -1:
                n = len(self.movies_id2name)
            top_movies = self._groupby_rating_by_film()
            if metric == 'average':
                top_movies = [(title, mean(ratings))
                              for title, ratings in top_movies.items()]
            else:
                top_movies = [(title, median(ratings))
                              for title, ratings in top_movies.items()]

            return dict(
                map(lambda x: (x[0], round(x[1], 2)),
                    sorted(top_movies, key=lambda x: x[1], reverse=True)[:n]))

        def _groupby_rating_by_film(self):
            self.init_mapping_movies()
            top_movies = defaultdict(list)
            for film_info in self.rating.read_csv():
                top_movies[self.movies_id2name[film_info['movieId']]].append(
                    float(film_info['rating']))
            return top_movies

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            if n == -1:
                n = len(self.movies_id2name)
            top_movies = self._groupby_rating_by_film()
            top_movies = [(title, var(ratings))
                          for title, ratings in top_movies.items()]

            return dict(
                map(lambda x: (x[0], round(x[1], 2)),
                    sorted(top_movies, key=lambda x: x[1], reverse=True)[:n]))

    class Users(Movies):
        """
        In this class, three methods should work.
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """

        def _groupby_rating_by_film(self):
            self.init_mapping_movies()
            top_movies = defaultdict(list)
            for film_info in self.rating.read_csv():
                top_movies[film_info['userId']].append(
                    float(film_info['rating']))
            return top_movies

        def top_controversial(self, n):
            return super().top_controversial(n)

        def dict_by_ratings(self, metric):
            return super().top_by_ratings(-1, metric)

        def dist_by_rating(self):
            ratings_distribution = Counter()
            for film_info in self.rating.read_csv():
                ratings_distribution[film_info['userId']] += 1
            return dict(ratings_distribution.most_common()[::-1])
