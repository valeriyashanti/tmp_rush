from movielens_analysis import CsvParser
from collections import Counter
from datetime import datetime
average=None
from movies import Movies as MoviesBase


class Ratings(CsvParser):
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        super().__init__(path_to_the_file)

    def is_valid_file(self):
        return set(self.columns) == set('userId,movieId,rating,timestamp'.split(','))

    def read_csv(self):
        for film_info in super(Ratings, self).read_csv():
            if not self.is_valid_file():
                raise TypeError
            yield film_info

    class Movies(MoviesBase):
        def __init__(self, movies_filename, rating):
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
            top_movies = Counter()
            for film_info in self.rating.read_csv():
                top_movies[self.movies_id2name[film_info['movieId']]] += 1
            return dict(top_movies.most_common()[:n])

        def top_by_ratings(self, n, metric=average):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            return top_movies
        
        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            return top_movies

    class Users:
        """
        In this class, three methods should work.
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
     Inherit from the class Movies. Several methods are similar to the methods from it.
        """
