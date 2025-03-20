import sys



class _Queries(object):
    def __init__(self):
        self.SearchMediaQuery = open("./app/graphql/queries/SearchMediaQuery.graphql", "rt").read()
        self.MediaQuery = open("./app/graphql/queries/MediaQuery.graphql", "rt").read()
        self.UserFavouritesQuery = open("./app/graphql/queries/UserFavouritesQuery.graphql", "rt").read()


Queries = _Queries()





