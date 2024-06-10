from api.rapidpro import pyRapid

df = pyRapid.runs.get_runs(
    before="2024-05-27 04:00:00", after="2024-05-27 01:00:00"
)

df.head(5)
