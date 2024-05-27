from api.aaq import pyAAQ

inbounds_ud = pyAAQ.inbounds_ud.get_inbounds_ud(
    start_datetime="2023-01-01 00:00:00",
    end_datetime="2023-12-31 00:00:00"
    )

inbounds_ud.head(5)
