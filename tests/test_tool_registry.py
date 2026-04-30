from harn import registry, tool


def test_tool_decorator_registers_function() -> None:
    @tool(name="echo", description="Echoes input")
    def echo(text: str) -> str:
        return text

    tools = {item.name: item for item in registry.list()}
    assert "echo" in tools
    assert tools["echo"].description == "Echoes input"
    assert tools["echo"].fn("ok") == "ok"
