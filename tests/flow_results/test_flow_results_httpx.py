import importlib
from unittest.mock import MagicMock, patch

import httpx
import pytest


@pytest.fixture(autouse=True)
def _set_required_env(monkeypatch):
    """Ensure required env vars exist to avoid import-time errors."""
    monkeypatch.setenv("FLOW_RESULTS_API_KEY", "test-key")
    monkeypatch.setenv("FLOW_RESULTS_API_BASE_URL", "http://test-api.com")


@pytest.fixture
def flow_results_httpx_module(_set_required_env):
    """Import the module under test."""
    return importlib.import_module(
        "rdw_ingestion_tools.api.flow_results.extensions.httpx"
    )


@pytest.fixture
def mock_client(monkeypatch, flow_results_httpx_module):
    """
    Patch the Client symbol used in the module under test
    and return the mock client.
    """
    client = MagicMock()
    client.__enter__.return_value = client
    client.__exit__.return_value = False

    monkeypatch.setattr(
        flow_results_httpx_module, "Client", lambda *args, **kwargs: client
    )
    return client


@pytest.fixture
def make_response():
    """
    Factory to construct a mock Response with a provided JSON payload
    and optional status error.
    """

    def _factory(json_data: dict, status_error: Exception | None = None):
        resp = MagicMock()
        resp.json.return_value = json_data
        if status_error is None:
            resp.raise_for_status.return_value = None
        else:
            resp.raise_for_status.side_effect = status_error
        return resp

    return _factory


def test_get_ids(flow_results_httpx_module, mock_client, make_response):
    json_payload = {
        "data": [
            {"id": "f-1"},
            {"id": "f-2"},
        ]
    }
    mock_client.get.return_value = make_response(json_payload)

    result = list(flow_results_httpx_module.get_ids(mock_client, org="acme", page=1))

    assert result == ["f-1", "f-2"]
    mock_client.get.assert_called_once_with("", params={"org": "acme", "page": 1})


def test_get_ids_error(flow_results_httpx_module, mock_client, make_response):
    req = httpx.Request("GET", "http://example.invalid")
    resp = httpx.Response(500, request=req)
    status_err = httpx.HTTPStatusError("Error", request=req, response=resp)
    mock_client.get.return_value = make_response({"data": []}, status_error=status_err)

    with pytest.raises(httpx.HTTPStatusError):
        list(flow_results_httpx_module.get_ids(mock_client))


def test_get_paginated_single_page(
    flow_results_httpx_module, mock_client, make_response
):
    json_payload = {
        "data": {
            "attributes": {"responses": [[{"a": 1}], [{"b": 2}]]},
            "relationships": {"links": {"next": None}},
        }
    }
    # Accessing ["next"] on a dict with None value won't raise AttributeError,
    # but our code only checks AttributeError. To keep a single page, we'll instead
    # make the relationships object raise AttributeError on __getitem__
    # in the pagination test.
    # For single-page, just ensure we don't provide a usable "next" URL
    # and call count is 1.
    mock_client.get.return_value = make_response(json_payload)

    result = list(flow_results_httpx_module.get_paginated(mock_client, "/packages/123"))

    assert result == [[{"a": 1}], [{"b": 2}]]
    mock_client.get.assert_called_once_with("/packages/123", params={})


def test_get_paginated_pagination(
    flow_results_httpx_module, mock_client, make_response
):
    # First page returns a next URL
    first_page = {
        "data": {
            "attributes": {"responses": [[{"a": 1}]]},
            "relationships": {
                "links": {"next": "https://api.example.com/packages/next-token"}
            },
        }
    }

    # Second page should trigger the break via AttributeError when accessing ["next"]
    bad_links = MagicMock()
    bad_links.__getitem__.side_effect = AttributeError
    second_page = {
        "data": {
            "attributes": {"responses": [[{"c": 3}]]},
            "relationships": bad_links,
        }
    }

    mock_client.get.side_effect = [
        make_response(first_page),
        make_response(second_page),
    ]

    result = list(
        flow_results_httpx_module.get_paginated(mock_client, "/packages/start", q="x")
    )

    assert result == [[{"a": 1}], [{"c": 3}]]
    assert mock_client.get.call_count == 2
    mock_client.get.assert_any_call("/packages/start", params={"q": "x"})
    # The second call should use the path part after "packages/"
    mock_client.get.assert_any_call("next-token", params={"q": "x"})


def test_get_paginated_kwargs_propagation(
    flow_results_httpx_module, mock_client, make_response
):
    json_payload = {
        "data": {
            "attributes": {"responses": []},
            "relationships": {"links": {"next": None}},
        }
    }
    mock_client.get.return_value = make_response(json_payload)

    list(
        flow_results_httpx_module.get_paginated(
            mock_client, "/packages/xyz", limit=50, cursor="abc"
        )
    )

    mock_client.get.assert_called_once_with(
        "/packages/xyz", params={"limit": 50, "cursor": "abc"}
    )


def test_get_paginated_retry_mechanism(
    flow_results_httpx_module, mock_client, make_response
):
    """Test that get_paginated uses RetryTransport for resilient HTTP requests."""
    pkg = importlib.import_module("rdw_ingestion_tools.api.flow_results.client")
    pkg.get_client.cache_clear()
    # Create a mock response
    json_payload = {
        "data": {
            "attributes": {"responses": [[{"a": 1}], [{"b": 2}]]},
            "relationships": {"links": {"next": None}},
        }
    }
    mock_response = make_response(json_payload)
    mock_client.get.return_value = mock_response

    # Mock the RetryTransport using the correct import path
    with (
        patch("rdw_ingestion_tools.api.flow_results.client.RetryTransport") as mock_rt,
        patch(
            "rdw_ingestion_tools.api.flow_results.client.Client",
            return_value=mock_client,
        ),
    ):
        pkg.get_client.cache_clear()  # ensure get_client uses patched make_client
        # Call the function
        result = list(
            flow_results_httpx_module.get_paginated(None, "http://test-api.com/data")
        )

        # Assertions
        assert len(result) == 2
        assert result == [[{"a": 1}], [{"b": 2}]]

        # Verify that RetryTransport was instantiated
        assert mock_rt.call_count == 1

        # Verify the call was made with correct parameters
        mock_client.get.assert_called_once_with("http://test-api.com/data", params={})


def test_make_client_uses_retrytransport():
    with patch("rdw_ingestion_tools.api.flow_results.client.RetryTransport") as mock_rt:
        from rdw_ingestion_tools.api.flow_results.client import make_client

        _ = make_client()
        assert mock_rt.call_count == 1
