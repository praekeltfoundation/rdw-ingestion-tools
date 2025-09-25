from api.rapidpro import pyRapid

runs = pyRapid().runs.get_runs(
    end_datetime="2024-06-22 00:00:10", start_datetime="2024-06-22 00:00:00"
)

print(runs.collect())
