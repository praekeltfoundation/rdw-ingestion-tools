from polars import (
    Int64,
    String,
)

statuses_schema = {
    "record_created_at": String,
    "partition_timestamp": String,
    "id": Int64,
    "description": String,
    "status": String,
    "timestamp": String,
    "uuid": String,
    "message_uuid": String,
    "raw_body": String,
    "errors": String,
    "message_id": Int64,
    "number_id": Int64,
    "inserted_at": String,
    "updated_at": String,
}
