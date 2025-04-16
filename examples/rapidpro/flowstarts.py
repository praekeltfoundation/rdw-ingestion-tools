from api.rapidpro import pyRapid

flowstarts = pyRapid().flow_starts.get_flowstarts(
    before="2023-01-02 00:00:00", after="2023-01-01 00:00:00"
)

flowstarts.head(5)
