from api.rapidpro import pyRapid

flowstarts = pyRapid().flow_starts.get_flowstarts(
    end_datetime="2023-01-02 00:00:00", start_datetime="2023-01-01 00:00:00"
)

print(flowstarts.collect())
