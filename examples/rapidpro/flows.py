from api.rapidpro import pyRapid

flows = pyRapid.flows.get_flows()

flows.head(5)
