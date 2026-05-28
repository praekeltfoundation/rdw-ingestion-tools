from api.maxim import pyMaxim

repositories_logs = pyMaxim().repositories_logs.get_repositories_logs(
    start_date="2026-05-26T13:00:00Z", end_date="2026-05-27T15:00:00Z", type="trace"
)

print(repositories_logs.collect())
