from api.turn_bq import pyTurnBQ

statuses = pyTurnBQ().statuses.get_statuses_by_updated_at(
    from_timestamp="2023-10-01T00:00:00", to_timestamp="2023-10-10T00:00:00"
)

print(statuses.head(5))
