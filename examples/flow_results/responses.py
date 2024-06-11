from datetime import datetime, timedelta

from api.flow_results import pyFlows

now = datetime.now()

end_time = now.isoformat()
start_time = (now - timedelta(days=1)).isoformat()

responses = pyFlows.responses.get_responses(
    start_time=start_time, end_time=end_time
)

print(f"Obtaining responses for dates: {start_time} to {end_time}.")

print(responses.keys())
