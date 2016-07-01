import random
import string
import json

DEFAULT_HEIGHT = 400
DEFAULT_WIDTH = 800

DB_HOST = ["localhost"]
DB_PORT = 27017


def get_random_string():
    random_letter = lambda: random.choice(string.ascii_letters)
    random_string = "".join([random_letter()
                             for el in range(10)])
    return random_string


def get_default_options(graph_type="lines"):
    """ default options """
    options = {"series": {"%s" % graph_type: {"show": "true"}},
               "legend": {"position": 'ne'},
               "title": "Chart"}
    return options


def get_db(db_name=None):
    """ GetDB - simple function to wrap getting a database
    connection from the connection pool.
    """
    import pymongo
    return pymongo.Connection(host=DB_HOST,
                              port=DB_PORT)[db_name]


class JSONEncoderForHTML(json.JSONEncoder):
    """An encoder that produces JSON safe to embed in HTML.
    To embed JSON content in, say, a script tag on a web page, the
    characters &, < and > should be escaped. They cannot be escaped
    with the usual entities (e.g. &amp;) because they are not expanded
    within <script> tags.
    """

    def encode(self, o):
        # Override JSONEncoder.encode because it has hacks for
        # performance that make things more complicated.
        chunks = self.iterencode(o, True)
        if self.ensure_ascii:
            return ''.join(chunks)
        else:
            return u''.join(chunks)

    def iterencode(self, o, _one_shot=False):
        try:
            chunks = super(JSONEncoderForHTML, self).iterencode(o, _one_shot)
        except TypeError:
            # for python 2.6 compatibility
            chunks = super(JSONEncoderForHTML, self).iterencode(o)
        for chunk in chunks:
            chunk = chunk.replace('&', '&amp;')
            chunk = chunk.replace('<', '&lt;')
            chunk = chunk.replace('>', '&gt;')
            yield chunk
