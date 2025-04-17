from api.turn_bq import pyTurnBQ

contacts = pyTurnBQ().contacts.get_contacts_by_id(contact_id=2350649091)

print(contacts.head(5))

contacts = pyTurnBQ().contacts.get_contacts_by_updated_at(
    from_timestamp="2023-10-01T00:00:00", to_timestamp="2023-10-10T00:00:00"
)

print(contacts.head(5))
