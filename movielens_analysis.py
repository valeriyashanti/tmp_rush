class InvalidCsv(Exception):
    pass


class CsvParser:
    def __init__(self, filename, sep=',', header=True):
        self.filename = filename
        self.sep = sep
        self.header = header
        self.columns = []
        self.count_features = None

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
        for row in self.open_csv():
            row_dict = {}
            flag = False
            column_idx = 0
            for obj in row.strip('\n').split(self.sep):
                try:
                    row_dict[self.columns[column_idx]] = row_dict.get(
                        self.columns[column_idx], '') + obj.strip('"')
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
            yield row_dict
