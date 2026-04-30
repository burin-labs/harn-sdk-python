from harn.stream import parse_sse_lines


def test_parse_sse_lines_json_payload() -> None:
    lines = iter(
        [
            "id: 1\n",
            "event: delta\n",
            'data: {"chunk":"he"}\n',
            "\n",
            "id: 2\n",
            'data: {"chunk":"llo"}\n',
            "\n",
        ]
    )
    events = list(parse_sse_lines(lines))
    assert len(events) == 2
    assert events[0].id == "1"
    assert events[0].event == "delta"
    assert events[0].data == {"chunk": "he"}
    assert events[1].data == {"chunk": "llo"}
