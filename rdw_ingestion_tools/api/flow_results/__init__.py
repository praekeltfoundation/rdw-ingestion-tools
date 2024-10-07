from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("FLOW_RESULTS_API_KEY")
BASE_URL = config_from_env("FLOW_RESULTS_API_BASE_URL")


headers = {"Authorization": f"Token {API_KEY}"}

client: Client = Client(base_url=BASE_URL, headers=headers)

from .main import pyFlows as pyFlows
