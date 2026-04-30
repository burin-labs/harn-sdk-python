from harn import HarnClient

# Deployment metadata can be published as an artifact + outcome record.
with HarnClient(base_url="http://localhost:8080") as client:
    artifact = client.register_artifact(
        body={"name": "pipeline-build", "mime_type": "application/json", "size": 2}
    )
    print("artifact", artifact)

    outcomes = client.list_outcomes(params={"artifact_id": artifact.get("id")})
    print("outcomes", outcomes)
