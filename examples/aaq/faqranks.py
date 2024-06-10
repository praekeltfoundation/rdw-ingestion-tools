from api.aaq import pyAAQ

faqranks = pyAAQ.inbounds.get_faqranks(
    start_datetime="2023-01-01 00:00:00", end_datetime="2023-12-31 00:00:00"
)

faqranks.head(5)
