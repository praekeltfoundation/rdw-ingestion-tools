from polars import Boolean, Float64, Int64, List, Schema, String, Struct, Utf8

urgency_rule = Struct(
    {
        "distance": Float64,
        "urgency_rule": Utf8,
    }
)

# Each element in the 'details' field below is a dictionary of format
# {
#   "{int in range(46)}": urgency_rule
# }
# The `details` for loop below recreates this for 100 such dictionaries
# (46 existing rules + space for new ones).
urgency_query_response = Struct(
    {
        "details": Struct({str(i): urgency_rule for i in range(100)}),
        "is_urgent": Boolean,
        "matched_rules": List(String),
        "response_datetime_utc": String,
        "urgency_response_id": Int64,
    }
)

urgency_queries_schema = Schema(
    {
        "message_datetime_utc": String,
        "message_text": String,
        "response": urgency_query_response,
        "urgency_query_id": Int64,
        "workspace_id": Int64,
    }
)
