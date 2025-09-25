from unittest.mock import Mock

import pytest

from rdw_ingestion_tools.api.rapidpro.extensions.httpx import get_paginated


@pytest.fixture
def mock_response():
    """Returns a mocked API response object"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    return mock_response


@pytest.fixture
def mock_client(mocker):
    """Returns a mocked Client object"""
    mock_client = mocker.patch(
        "rdw_ingestion_tools.api.rapidpro.extensions.httpx.Client"
    )
    return mock_client


def test_get_paginated_empty_response(mock_client, mock_response):
    """
    Tests that the pagination function can handle an empty response.

    """
    mock_response.json.return_value = {"next": None, "previous": None, "results": []}

    mock_client.get.return_value = mock_response

    list(get_paginated(client=mock_client, url="https://test.com"))

    mock_client.get.assert_called_once_with("https://test.com", params={})


def test_get_paginated_cursor_usage(mock_client, mock_response):
    """
    Tests that the pagination function call sthe API with the expected cursor.

    """

    # First mock response object
    mock_response.json.return_value = {
        "results": [{"id": 1}],
        "next": "https://test.com.json?after=2023-01-01+00%3A00%3A00&before=2023-03-01+00%3A00%3A50&cursor=cD0yMDIzLTEwLTI3VDEwJTNBMzAlM0EwMC4wMDAwMDBa&extra_param=1",
    }

    # Second mock response object
    mock_response2 = Mock()
    mock_response2.status_code = 200
    mock_response2.raise_for_status.return_value = None
    mock_response2.json.return_value = {"results": [{"id": 3}], "next": None}

    mock_client.get.side_effect = [mock_response, mock_response2]

    generator = get_paginated(client=mock_client, url="https://test.com", foo="bar")

    # First call
    next(generator)
    mock_client.get.assert_called_with("https://test.com", params={"foo": "bar"})

    # Second call
    next(generator)
    mock_client.get.assert_called_with(
        "https://test.com",
        params={"foo": "bar", "cursor": "cD0yMDIzLTEwLTI3VDEwJTNBMzAlM0EwMC4wMDAwMDBa"},
    )


def test_get_paginated_additional_kwargs(mock_client, mock_response):
    """
    Tests that the pagination function can handle additional kwargs.

    """
    mock_response.json.return_value = {"results": [{"id": 3}], "next": None}

    mock_client.get.return_value = mock_response

    list(get_paginated(client=mock_client, url="https://test.com", foo="bar"))

    mock_client.get.assert_called_once_with("https://test.com", params={"foo": "bar"})
