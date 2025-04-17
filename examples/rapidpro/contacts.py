from api.rapidpro import pyRapid

contacts = pyRapid().contacts.get_contacts(
    before="2023-01-02 00:00:00", after="2023-01-01 00:00:00"
)

contacts.head(5)
