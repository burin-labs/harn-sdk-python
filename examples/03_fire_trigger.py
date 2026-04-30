from harn import HarnClient

# Trigger-like event ingestion can be modeled via memory/session message writes.
with HarnClient(base_url="http://localhost:8080") as client:
    created = client.create_memory(
        body={
            "namespace": "triggers",
            "key": "manual.release",
            "value": {"version": "1.2.3", "source": "sdk-example"},
        }
    )
    print(created)
