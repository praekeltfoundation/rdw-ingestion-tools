from api.aaqv2 import pyAAQV2

urgency_rules = pyAAQV2().urgency_rules.get_urgency_rules()

print(urgency_rules.collect().head(5))
