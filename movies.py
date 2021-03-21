import re
from collections import Counter


class InvalidCsv(Exception):
    pass


class CsvParser:
    def __init__(self, filename, sep=',', header=True):
        self.filename = filename
        self.sep = sep
        self.header = header
        self.columns = []
        self.count_features = None
        self.csv_data = None

    def open_csv(self):
        with open(self.filename) as fd:
            if self.header:
                self.columns = next(fd).strip('\n').split(',')
                self.count_features = len(self.columns)
            else:
                self.columns = range(int(1e6))
            for row in fd:
                yield row.strip()

    def read_csv(self):
        result_data = []
        if self.csv_data is not None:
            return self.csv_data
        for row in self.open_csv():
            row_dict = {}
            flag = False
            column_idx = 0
            for obj in row.strip('\n').split(self.sep):
                try:
                    row_dict[self.columns[column_idx]] = obj.strip('"')
                except IndexError:
                    raise InvalidCsv

                if obj.count('"') == 1:
                    flag = not flag

                if flag:
                    row_dict[self.columns[column_idx]] += self.sep
                else:
                    column_idx += 1
            if self.count_features is None:
                self.count_features = len(row_dict)
            if len(row_dict) != self.count_features:
                raise InvalidCsv
            result_data.append(row_dict)
        self.csv_data = result_data
        return self.csv_data


class Movies(CsvParser):
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        super().__init__(path_to_the_file)

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
            film_name = re.sub(r'\(\d{4}\)$', '', film_info['title']).strip()
            movies[film_name] = len(self._get_film_genre(film_info))
        return dict(movies.most_common()[:n])
