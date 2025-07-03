from polars import (
    Boolean,
    Int64,
    String,
)

cards_schema = {
    "record_created_at": String,
    "partition_timestamp": String,
    "id": Int64,
    "content": String,
    "is_deleted": Boolean,
    "language": String,
    "save_to_field": String,
    "title": String,
    "type": String,
    "error_message": String,
    "metadata_": String,
    "uuid": String,
    "number_id": Int64,
    "inserted_at": String,
    "updated_at": String,
}
