from api.turn import pyTurn

start = "2024-01-01T00:00:00+00:00"
end = "2024-01-01T05:00:00+00:00"

contacts = pyTurn.contacts.get_contacts(start=start, end=end)

print(contacts.head(5))
