from api.rapidpro import pyRapid

groups = pyRapid().groups.get_groups()

print(groups.collect())
