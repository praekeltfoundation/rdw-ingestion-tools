from datetime import datetime, timedelta

from api.flow_results import pyFlows

end_time = datetime.now().isoformat()
start_time = (datetime.now() - timedelta(1)).isoformat()

responses = pyFlows.responses.get_responses(
    start_time=start_time, end_time=end_time
)

print(
    "Obtaining responses for dates: ",
    start_time,
    " to ",
    end_time,
    "\n\n",
    responses.keys(),
)
