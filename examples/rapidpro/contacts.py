from api.rapidpro import pyRapid

df = pyRapid.contacts.get_contacts(
    before="2023-01-02 00:00:00", after="2023-01-01 00:00:00"
)

df.head(5)
