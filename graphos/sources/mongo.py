""" Mongodb Plot Data Source """

from .base import BaseDataSource


def get_row(doc, fields):
    current_row = []
    for i in range(len(fields)):
        try:
            field = doc[fields[i]]
        except KeyError:
            field = ""
        current_row.append(field)
    return current_row


class MongoDBDataSource(BaseDataSource):
    """ MongoDBDataSource """

    def __init__(self,
                 cursor,
                 fields,
                 *args,
                 **kwargs):

        self.cursor = cursor
        self.fields = fields
        self._doc_list = []

    def get_data(self):
        if self._doc_list:
            return self._doc_list
        doc_list = []
        doc_list.append(self.fields)
        for doc in self.cursor:
            current_row = get_row(doc, self.fields)
            doc_list.append(current_row)
        self._doc_list = doc_list
        return doc_list

    def get_header(self):
        return self.fields

    def get_first_column(self):
        return self.fields
