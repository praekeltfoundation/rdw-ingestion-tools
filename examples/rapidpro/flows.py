from api.rapidpro import pyRapid

flows = pyRapid().flows.get_flows()

print(flows.collect())
