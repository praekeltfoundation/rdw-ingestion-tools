from datetime import datetime, timedelta

from api.turn import pyTurn

end = datetime.now().isoformat()
start = (datetime.now() - timedelta(2)).isoformat()

messages = pyTurn.messages.get_messages(start=start, end=end)

messages.keys()
