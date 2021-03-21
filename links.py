from bs4 import BeautifulSoup as bs
from movielens_analysis import CsvParser
from collections import Counter
import requests
import json


class Links(CsvParser):
    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file):
        self.data = []
        super().__init__(path_to_the_file)
        self.data = list(super().read_csv())

    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...]
            for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        result = []

        def parse_movie(imdbId):

            def get_info(soap_tag):
                info = str(soap_tag)
                i = 0
                l = info.__len__()
                while i < l and info[i] != '>':
                    i += 1
                start = i + 1
                while i < l and info[i] != '<':
                    i += 1
                return (info[start:i] if i < l else info).strip()

            link = f'https://www.imdb.com/title/tt{imdbId}/'
            raw_0 = requests.get(link).text

            content = bs(raw_0, features="html.parser")
            raw_1 = content.find(
                'script', attrs={'type': "application/ld+json"})

            dict_info = json.loads(raw_1.contents[0])
            raw_2 = content.find_all('div', attrs={'class': "txt-block"})
            for e in raw_2:
                pair = [el for el in e.contents if el != '\n'][:2]
                dict_info[get_info(pair[0])] = get_info(pair[1])
            return dict_info

        list_of_movies = sorted(list_of_movies, reverse=True)
        for movie in list_of_movies:
            imdb = None
            for row in self.data:
                movie_id = row['movieId']
                imdb_id = row['imdbId']
                if movie == movie_id:
                    imdb = imdb_id
            if imdb is None:
                raise ValueError(f'Incorrect movie_id: {movie}')
            dict_info = parse_movie(imdb)
            dict_v = {movie: ""}

            for field in list_of_fields:
                field_to_lower = field
                if field_to_lower in dict_info.keys():
                    by_key = dict_info[field_to_lower]
                    if isinstance(by_key, list):
                        for key in by_key:
                            if "name" in key:
                                dict_v[key["name"]] = ""
                    elif isinstance(by_key, dict):
                        dict_v[dict_info[field_to_lower]["name"]] = ""
                    else:
                        dict_v[by_key] = ""
            result.append(list(dict_v.keys()))
        return result

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and
        the values are numberы of movies created by them. Sort it by numbers descendingly.
        """
        big_tags = Counter()

        movie_ids = []
        for row in self.data:
            movie_ids.append(row['movieId'])
        directors = self.get_imdb(movie_ids, ["director"])
        for director in directors:
            print(director)
            # for tag_list in
            #     big_tags[tag_list] += 1
        return dict(big_tags.most_common(n))

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        pass

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        pass

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """
        pass

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles
            and the values are the budgets divided by their runtime.
        The budgets can be in different currencies – do not pay attention to it.
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        pass


if __name__ == '__main__':
    print(Links("ml-latest-small/links.csv").top_directors(1))
