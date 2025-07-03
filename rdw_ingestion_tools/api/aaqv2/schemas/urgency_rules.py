from polars import Int64, String, Struct

urgency_rules_schema = {
    "urgency_rule_metadata": Struct,
    "urgency_rule_text": String,
    "created_datetime_utc": String,
    "updated_datetime_utc": String,
    "urgency_rule_id": Int64,
    "workspace_id": Int64,
}
