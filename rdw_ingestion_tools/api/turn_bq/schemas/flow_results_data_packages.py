from polars import (
    Int64,
    String,
)

flow_results_data_packages_schema = {
    "record_created_at": String,
    "partition_timestamp": String,
    "uuid": String,
    "flow_results_specification_version": String,
    "name": String,
    "resources": String,
    "stack_uuid": String,
    "title": String,
    "profile": String,
    "number_id": Int64,
    "stack_container_uuid": String,
    "inserted_at": String,
    "updated_at": String,
}
