from api.rapidpro import pyRapid

fields = pyRapid().fields.get_fields()

fields.head(5)
