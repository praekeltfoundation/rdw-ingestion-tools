from polars import (
    Boolean,
    Int64,
    String,
)

contacts_schema = {
    "record_created_at": String,
    "partition_timestamp": String,
    "id": Int64,
    "uuid": String,
    "type": String,
    "urn": String,
    "details": String,
    "number_id": Int64,
    "organisation_id": Int64,
    "is_fallback_active": Boolean,
    "failure_count": Int64,
    "inserted_at": String,
    "updated_at": String,
}
