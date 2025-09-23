from api.rapidpro import pyRapid

contacts = pyRapid().contacts.get_contacts(
    end_datetime="2023-01-01 01:00:50", start_datetime="2023-01-01 00:00:00"
)

print(contacts.collect())
