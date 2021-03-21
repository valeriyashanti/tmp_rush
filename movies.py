import re
from collections import Counter
from movielens_analysis import CsvParser


class Movies(CsvParser):
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        super().__init__(path_to_the_file)

    def is_valid_file(self):
        return set(self.columns) == set('movieId,title,genres'.split(','))

    def read_csv(self):
        for film_info in super(Movies, self).read_csv():
            if not self.is_valid_file():
                raise TypeError
            # film_info['film_name'] = re.sub(r'\(\d{4}\)$', '', film_info['title']).strip('"\n ')
            yield film_info

    def dist_by_release(self):
        """
        The method returns a dict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        release_years = Counter()
        for film_info in self.read_csv():
            try:
                year = int(re.findall(r'\((\d{4})\)', film_info['title'])[-1])
            except IndexError:
                continue
            release_years[year] += 1
        return dict(release_years.most_common())

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """
        genres = Counter()
        for film_info in self.read_csv():

            for genre in self._get_film_genre(film_info):
                genres[genre] += 1
        return dict(genres.most_common())

    @staticmethod
    def _get_film_genre(film_info: dict):
        if film_info['genres'] == '(no genres listed)':
            return []
        return film_info['genres'].split('|')

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        movies = Counter()
        for film_info in self.read_csv():
            # movies[film_info['film_name']] = len(self._get_film_genre(film_info))
            movies[film_info['title']] = len(self._get_film_genre(film_info))
        return dict(movies.most_common()[:n])
