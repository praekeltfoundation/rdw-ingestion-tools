from api.turn_bq import pyTurnBQ

messages = pyTurnBQ().messages.get_messages_by_updated_at(
    from_timestamp="2023-10-01T00:00:00", to_timestamp="2023-10-10T00:00:00"
)

print(messages.collect().head(5))
