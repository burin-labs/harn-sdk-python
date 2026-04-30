from harn import HarnClient

session_id = "sess_123"

with HarnClient(base_url="http://localhost:8080") as client:
    for event in client.stream_session_events(session_id):
        print(event.event, event.data)
