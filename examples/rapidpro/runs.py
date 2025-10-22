from api.rapidpro import pyRapid

runs = pyRapid().runs.get_runs(
    end_datetime="2025-10-16 00:00:00", start_datetime="2025-10-15 00:00:00"
)

print(runs.collect())
