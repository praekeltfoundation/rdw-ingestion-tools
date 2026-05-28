from api.maxim import pyMaxim

repositories = pyMaxim().repositories.get_repositories()

print(repositories.collect())
