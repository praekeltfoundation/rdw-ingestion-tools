from api.turn_bq import pyTurnBQ

chats = pyTurnBQ().chats.get_chats_by_id(chat_id=1531207597)

print(chats.collect().head(5))

chats = pyTurnBQ().chats.get_chats_by_updated_at(
    from_timestamp="2023-10-01T00:00:00", to_timestamp="2023-10-01T00:50:00"
)

print(chats.collect().head(5))
