from polars import Boolean, Int64, List, String, Struct

contents_schema = {
    "content_metadata": Struct,
    "content_tags": List(String),
    "content_text": String,
    "content_title": String,
    "is_archived": Boolean,
    "content_id": Int64,
    "display_number": Int64,
    "created_datetime_utc": String,
    "negative_votes": Int64,
    "positive_votes": Int64,
    "updated_datetime_utc": String,
    "workspace_id": Int64,
}
