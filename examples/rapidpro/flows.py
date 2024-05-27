from api.rapidpro import pyRapid

df = pyRapid.flows.get_flows()

df.head(5)
