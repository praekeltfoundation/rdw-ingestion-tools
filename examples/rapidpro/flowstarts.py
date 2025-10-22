from api.rapidpro import pyRapid

flowstarts = pyRapid().flow_starts.get_flowstarts(
    end_datetime="2025-10-16 00:00:00", start_datetime="2025-10-15 00:00:00"
)

print(flowstarts.collect())
