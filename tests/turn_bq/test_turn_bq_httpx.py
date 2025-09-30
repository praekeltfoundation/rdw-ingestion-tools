import importlib
from unittest.mock import MagicMock, patch

import httpx
import pytest


@pytest.fixture(autouse=True)
def _set_required_env(monkeypatch):
    """Ensure required env vars exist to avoid import-time errors."""
    monkeypatch.setenv("TURN_BQ_API_KEY", "test-key")
    monkeypatch.setenv("TURN_BQ_API_BASE_URL", "http://test-api.com")


@pytest.fixture
def turn_bq_httpx_module(_set_required_env):
    """Import the module under test after env is set and return it."""
    return importlib.import_module("rdw_ingestion_tools.api.turn_bq.extensions.httpx")


@pytest.fixture
def mock_client(monkeypatch, turn_bq_httpx_module):
    """Fixture that patches the Client used in the module under test and returns it."""
    client = MagicMock()
    client.__enter__.return_value = client
    client.__exit__.return_value = False

    monkeypatch.setattr(turn_bq_httpx_module, "Client", lambda *args, **kwargs: client)
    return client


@pytest.fixture
def make_mock_response():
    """Factory to build a mock httpx.Response-like object.

    Usage: make_mock_response(items=[...], page=1, pages=1, status_error=None)
    """

    def _factory(*, items, page, pages, status_error: Exception | None = None):
        resp = MagicMock()
        resp.json.return_value = {
            "items": items,
            "page": page,
            "pages": pages,
        }
        if status_error is None:
            resp.raise_for_status.return_value = None
        else:
            resp.raise_for_status.side_effect = status_error
        return resp

    return _factory


def test_get_paginated(turn_bq_httpx_module, mock_client, make_mock_response):
    """Test that get_paginated yields items from a successful response."""
    mock_response = make_mock_response(items=[{"id": 1}, {"id": 2}], page=1, pages=1)
    mock_client.get.return_value = mock_response

    result = list(
        turn_bq_httpx_module.get_paginated(mock_client, "http://test-api.com/data")
    )

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2
    mock_client.get.assert_called_once_with(
        "http://test-api.com/data", params={"page": 1, "size": 1000}
    )


def test_get_paginated_error_handling(
    turn_bq_httpx_module, mock_client, make_mock_response
):
    """Test that get_paginated raises an exception when the API returns an error."""
    req = httpx.Request("GET", "http://test-api.com/data")
    resp = httpx.Response(500, request=req)
    status_err = httpx.HTTPStatusError("Error", request=req, response=resp)

    mock_response = make_mock_response(
        items=[], page=1, pages=1, status_error=status_err
    )
    mock_client.get.return_value = mock_response

    with pytest.raises(httpx.HTTPStatusError):
        list(
            turn_bq_httpx_module.get_paginated(mock_client, "http://test-api.com/data")
        )


def test_get_paginated_pagination(
    turn_bq_httpx_module, mock_client, make_mock_response
):
    """Test that get_paginated correctly handles pagination across multiple pages."""
    mock_response_page1 = make_mock_response(
        items=[{"id": 1}, {"id": 2}], page=1, pages=2
    )
    mock_response_page2 = make_mock_response(
        items=[{"id": 3}, {"id": 4}], page=2, pages=2
    )

    mock_client.get.side_effect = [mock_response_page1, mock_response_page2]

    result = list(
        turn_bq_httpx_module.get_paginated(
            mock_client, "http://test-api.com/data", page_size=2
        )
    )

    assert len(result) == 4
    assert [item["id"] for item in result] == [1, 2, 3, 4]
    assert mock_client.get.call_count == 2
    mock_client.get.assert_any_call(
        "http://test-api.com/data", params={"page": 1, "size": 2}
    )
    mock_client.get.assert_any_call(
        "http://test-api.com/data", params={"page": 2, "size": 2}
    )


def test_get_paginated_with_additional_params(
    turn_bq_httpx_module, mock_client, make_mock_response
):
    """Test that get_paginated correctly passes additional parameters to the API."""
    mock_response = make_mock_response(items=[{"id": 1}], page=1, pages=1)
    mock_client.get.return_value = mock_response

    list(
        turn_bq_httpx_module.get_paginated(
            mock_client,
            "http://test-api.com/data",
            param1="value1",
            param2=123,
        )
    )


def test_get_paginated_retry_mechanism(
    turn_bq_httpx_module, make_mock_response, mock_client
):
    pkg = importlib.import_module("rdw_ingestion_tools.api.turn_bq.client")
    pkg.get_client.cache_clear()

    mock_response = make_mock_response(items=[{"id": 1}], page=1, pages=1)
    mock_client.get.return_value = mock_response

    with patch(
        "rdw_ingestion_tools.api.turn_bq.client.Client", return_value=mock_client
    ):
        pkg.get_client.cache_clear()  # ensure get_client uses patched make_client
        result = list(
            turn_bq_httpx_module.get_paginated(mock_client, "http://test-api.com/data")
        )

    assert len(result) == 1
    assert result[0]["id"] == 1
    mock_client.get.assert_called_once_with(
        "http://test-api.com/data", params={"page": 1, "size": 1000}
    )


def test_make_client_uses_retrytransport():
    with patch("rdw_ingestion_tools.api.turn_bq.client.RetryTransport") as mock_rt:
        from rdw_ingestion_tools.api.turn_bq.client import make_client

        _ = make_client()
        assert mock_rt.call_count == 1
