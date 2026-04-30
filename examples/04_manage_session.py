from harn import HarnClient

with HarnClient(base_url="http://localhost:8080") as client:
    session = client.create_session(body={"name": "sdk-demo"})
    sid = session["id"]

    client.append_session_message(sid, body={"role": "user", "content": "Hello"})
    messages = client.list_session_messages(sid)
    print(messages)

    client.close_session(sid)
