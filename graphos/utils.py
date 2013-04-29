

def get_default_options(graph_type="lines"):
    """ default options """
    options = {"series": {"%s" % graph_type: {"show": "true"}},
               "legend": {"position": 'ne'},
               "title": "Chart"}
    return options
