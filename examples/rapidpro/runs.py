from api.rapidpro import pyRapid

runs = pyRapid.runs.get_runs(before="2024-10-01 04:00:00", after="2024-10-01 01:00:00")

runs.head(5)
