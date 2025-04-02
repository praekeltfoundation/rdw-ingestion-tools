from api.aaqv2 import pyAAQV2

start_date = "2025-04-01T00:00:00"
end_date = "2025-04-02T00:00:00"

queries = pyAAQV2.queries.get_queries(start_date=start_date, end_date=end_date)

queries.head(5)
