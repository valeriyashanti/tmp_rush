from movielens_analysis import CsvParser
from collections import Counter


class Tags(CsvParser):
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        super().__init__(path_to_the_file)

    def is_valid_file(self):
        return set(self.columns) == set('userId,movieId,tag,timestamp'.split(','))

    def read_csv(self):
        for tags in super(Tags, self).read_csv():
            if not self.is_valid_file():
                raise TypeError
            tags['tag'] = tags['tag'].lower()
            yield tags

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = Counter()
        for tags in self.read_csv():
            tags_list = self._get_tags(tags)
            big_tags[" ".join(tags_list)] = len(tags_list)
        return dict(big_tags.most_common(n))

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = Counter()
        for tags in self.read_csv():
            for tag_list in self._get_tags(tags):
                big_tags[tag_list] = len(tag_list)
        return list(dict(big_tags.most_common(n)).keys())

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        big_tags = list(set(self.most_words(n)) & set(self.longest(n)))
        return big_tags

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        big_tags = Counter()
        for tags in self.read_csv():
            for tag_list in self._get_tags(tags):
                big_tags[tag_list] += 1
        return dict(big_tags.most_common(n))

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        word = str(word).lower()
        tags_with = set()
        for tags in self.read_csv():
            tag_list = tags['tag']
            if self.contains_tag(str(tag_list), word):
                tags_with.add(str(tag_list))
        return sorted(tags_with)

    @staticmethod
    def _get_tags(tags: dict):
        return tags['tag'].split(' ')

    @staticmethod
    def contains_tag(tag_list, word):
        for tag in tag_list.split(" "):
            if tag == word:
                return True
        return False
