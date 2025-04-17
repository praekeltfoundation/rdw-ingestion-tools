from api.aaq import pyAAQ

inbounds = pyAAQ().inbounds.get_inbounds(
    start_datetime="2023-01-01 00:00:00", end_datetime="2023-02-01 00:00:00"
)

inbounds.head(5)
