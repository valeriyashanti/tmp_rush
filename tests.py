from ratings import Ratings
from movies import Movies
from tags import Tags
from collections import Counter


movies = Movies('ml-latest-small/movies.csv')
rating = Ratings('ml-latest-small/ratings.csv', 'ml-latest-small/movies.csv')
tags = Tags('ml-latest-small/tags.csv')


class Tests:
    def test_movies_dist_by_release(self):
        result = movies.dist_by_release()
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {int}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_movies_dist_by_genres(self):
        result = movies.dist_by_genres()
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_movies_most_genres(self):
        result = movies.most_genres(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_rating_dist_by_year(self):
        result = rating.get_movies().dist_by_year()
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {int}) and
                sorted(result.values(), reverse=False) == list(result.values()))

    def test_rating_dist_by_rating(self):
        result = rating.get_movies().dist_by_rating()
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {float}) and
                sorted(result.values(), reverse=False) == list(result.values()))

    def test_rating_top_by_num_of_ratings(self):
        result = rating.get_movies().top_by_num_of_ratings(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_rating_top_by_ratings(self):
        for metric in ['average', 'median']:
            result = rating.get_movies().top_by_ratings(500, metric)
            assert (isinstance(result, dict) and
                    (set(map(type, result.values())) == {float} and
                     set(map(type, result.keys())) == {str}) and
                    sorted(result.values(), reverse=True) == list(result.values()))

    def test_rating_top_controversial(self):
        result = rating.get_movies().top_controversial(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {float} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_tags_most_words(self):
        result = tags.most_words(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_tags_longest(self):
        big_tags = Counter()
        for tag_s in tags.read_csv():
            for tag_list in tags._get_tags(tag_s):
                big_tags[tag_list] = len(tag_list)
        result = tags.longest(10)
        print(sorted(dict(big_tags).items(), reverse=True, key=lambda x: x[1])[:10])
        assert (isinstance(result, list) and
                set(map(type, result)) == {str} and
                [el[0] for el in sorted(dict(big_tags).items(),
                                        reverse=True, key=lambda x: x[1])[:10]] == list(result))

    def test_tags_most_words_and_longest(self):
        result = tags.most_words_and_longest(1000)
        assert (isinstance(result, list) and
                set(map(type, result)) == {str})

    def test_tags_most_popular(self):
        result = tags.most_popular(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_tags_with(self):
        result = tags.tags_with('Netflix')
        assert (isinstance(result, list) and
                set(map(type, result)) == {str} and
                sorted(result, reverse=False) == list(result))
