from harn.auth import APIKeyCredential, AmbientCredential


def test_api_key_credential_returns_value() -> None:
    cred = APIKeyCredential("abc")
    assert cred.get_token() == "abc"


def test_ambient_credential_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("HARN_API_KEY", "xyz")
    cred = AmbientCredential()
    assert cred.get_token() == "xyz"


def test_ambient_credential_missing(monkeypatch) -> None:
    monkeypatch.delenv("HARN_API_KEY", raising=False)
    cred = AmbientCredential()
    assert cred.get_token() is None
