from harn import HarnClient

# In Harn, workflow execution is submitted as a task.
with HarnClient(base_url="http://localhost:8080") as client:
    result = client.submit_task(
        body={
            "workflow": {
                "name": "default",
                "input": {"prompt": "Summarize release notes"},
            },
            "mode": "sync",
        }
    )
    print(result)
