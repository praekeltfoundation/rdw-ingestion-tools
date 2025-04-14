from api.aaqv2 import pyAAQV2

contents = pyAAQV2().contents.get_contents()

print(contents.head(5))
