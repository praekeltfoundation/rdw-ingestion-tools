from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("MAXIM_API_KEY")
BASE_URL = config_from_env("MAXIM_BASE_URL")
WORKSPACE_ID = config_from_env("WORKSPACE_ID")

headers = {"x-maxim-api-key": API_KEY, "Content-Type": "application/json"}

params = {"workspaceId": WORKSPACE_ID}

client: Client = Client(base_url=BASE_URL, headers=headers, params=params)

from .main import pyMaxim as pyMaxim
