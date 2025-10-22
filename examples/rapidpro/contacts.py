from api.rapidpro import pyRapid

contacts = pyRapid().contacts.get_contacts(
    end_datetime="2025-10-16 00:00:00", start_datetime="2025-10-10 00:00:00"
)

print(contacts.collect())
