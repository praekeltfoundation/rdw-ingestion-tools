from polars import (
    Int64,
    String,
)

flow_results_schema = {
    "record_created_at": String,
    "partition_timestamp": String,
    "uuid": String,
    "question_id": String,
    "response": String,
    "response_metadata": String,
    "stack_uuid": String,
    "session_id": String,
    "number_id": Int64,
    "contact_id": Int64,
    "stack_container_uuid": String,
    "inserted_at": String,
    "updated_at": String,
}
