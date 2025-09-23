from api.rapidpro import pyRapid

fields = pyRapid().fields.get_fields()

print(fields.collect())
