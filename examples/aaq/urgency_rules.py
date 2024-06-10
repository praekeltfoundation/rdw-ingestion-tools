from api.aaq import pyAAQ

urgency_rules = pyAAQ.urgency_rules.get_urgency_rules()

urgency_rules.head(5)
