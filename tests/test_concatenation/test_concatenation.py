from polars import LazyFrame, Object, String
from polars.testing import assert_frame_equal

from rdw_ingestion_tools.api import concatenate_to_string_lazyframe, get_polars_schema


def test_get_polars_schema_empty_data():
    """
    Tests that schemas generated for empty responses are empty dictionaries.
    """
    data = [{}]
    schema = get_polars_schema(object_columns=[], data=data)

    assert schema == {}


def test_get_polars_schema_primitive_types():
    """
    Tests that schemas generated from response data use type `String`
    for all primitive types.
    """
    data = [
        {
            "col1": 1,
            "col2": 2.0,
            "col3": False,
            "col4": None,
            "col5": "string",
            "col6": "2025-01-01",
        }
    ]

    schema = get_polars_schema(object_columns=[], data=data)

    expected_schema = {
        "col1": String,
        "col2": String,
        "col3": String,
        "col4": String,
        "col5": String,
        "col6": String,
    }

    assert schema == expected_schema


def test_get_polars_schema_list_types():
    """
    Tests that generated schemas from response data use type `Object`
    for list columns.
    """
    data = [{"col1": [1, 2, 3], "col2": [{"key": "value"}], "col3": False}]

    schema = get_polars_schema(object_columns=["col1", "col2"], data=data)

    expected_schema = {"col1": Object, "col2": Object, "col3": String}

    assert schema == expected_schema


def test_get_polars_schema_json_types():
    """
    Tests that generated schemas from response data with JSON columns
    normalise the column names in the schema.
    """
    data = [{"col1": {"key": {"inner_key": "value"}}, "col2": {"key": "value"}}]

    schema = get_polars_schema(object_columns=[], data=data)

    expected_schema = {"col1_key_inner_key": String, "col2_key": String}

    assert schema == expected_schema


def test_concatenate_to_string_lazyframe():
    """
    Tests that response data is concatenated and normalised into LazyFrames
    with column type `String`.
    """
    data = [
        {"col1": 1, "col2": [1, 2, 3], "col3": {"key": "value1"}},
        {"col1": 2, "col2": [1, 2, 3], "col3": {"key": "value2"}},
    ]

    lf = concatenate_to_string_lazyframe(objs=data, object_columns=["col2"])

    expected_lf = LazyFrame(
        {
            "col1": ["1", "2"],
            "col2": ["[1, 2, 3]", "[1, 2, 3]"],
            "col3_key": ["value1", "value2"],
        }
    )

    assert_frame_equal(lf, expected_lf)


def test_concatenate_to_string_lazyframe_empty_response():
    """
    Tests that concatenate_to_string_lazyframe returns an empty LazyFrame for
    empty response data.
    """
    data = [{}]

    lf = concatenate_to_string_lazyframe(objs=data, object_columns=[])

    assert_frame_equal(lf, LazyFrame(data=[[]], schema={}))
