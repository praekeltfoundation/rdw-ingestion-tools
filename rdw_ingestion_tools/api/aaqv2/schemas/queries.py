from polars import Field, Float64, Int64, List, String, Struct

search_results = Struct(
    [
        Field(
            "0",
            Struct(
                [
                    Field("title", String),
                    Field("text", String),
                    Field("id", Int64),
                    Field("distance", Float64),
                ]
            ),
        ),
        Field(
            "1",
            Struct(
                [
                    Field("title", String),
                    Field("text", String),
                    Field("id", Int64),
                    Field("distance", Float64),
                ]
            ),
        ),
        Field(
            "2",
            Struct(
                [
                    Field("title", String),
                    Field("text", String),
                    Field("id", Int64),
                    Field("distance", Float64),
                ]
            ),
        ),
        Field(
            "3",
            Struct(
                [
                    Field("title", String),
                    Field("text", String),
                    Field("id", Int64),
                    Field("distance", Float64),
                ]
            ),
        ),
    ]
)


content_feedback = Struct(
    [
        Field("content_id", Int64),
        Field("feedback_datetime_utc", String),
        Field("feedback_id", Int64),
        Field("feedback_sentiment", String),
        Field("feedback_text", String),
    ]
)

query_response = Struct(
    [
        Field("llm_response", String),
        Field("response_datetime_utc", String),
        Field("response_id", Int64),
        Field("search_results", search_results),
    ]
)

response_feedback = Struct(
    [
        Field("feedback_datetime_utc", String),
        Field("feedback_id", Int64),
        Field("feedback_sentiment", String),
        Field("feedback_text", String),
    ]
)

queries_schema = {
    "content_feedback": List(content_feedback),
    "query_datetime_utc": String,
    "query_id": Int64,
    "query_metadata": Struct,
    "query_text": String,
    "response": List(query_response),
    "response_feedback": List(response_feedback),
    "workspace_id": Int64,
}
