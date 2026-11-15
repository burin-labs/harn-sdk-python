"""Process exit and reaping are distinct pidfd events."""

import os
import queue
import select
import subprocess
import sys
import threading
from types import SimpleNamespace

import pytest

from scripts import codegen_product_native as product


@pytest.mark.skipif(not hasattr(os, "pidfd_open"), reason="Linux pidfd observation")
def test_worker_reap_observation_waits_for_reaping_after_a_known_exit(monkeypatch):
    child = subprocess.Popen([sys.executable, "-c", "pass"])
    registered, terminal = queue.Queue(), queue.Queue()
    parent_reaped = threading.Event()
    observer = None
    descriptor = os.pidfd_open(child.pid)
    actual_poll = select.poll

    class ObservedPoll:
        def __init__(self):
            self.poller = actual_poll()

        def register(self, descriptor, events):
            self.poller.register(descriptor, events)
            self.events = events
            registered.put(("registered", events))

        def modify(self, descriptor, events):
            self.register(descriptor, events)

        def poll(self, timeout):
            assert 0 <= timeout <= 30000
            if self.events == select.POLLHUP:
                assert parent_reaped.wait(timeout=30)
            return self.poller.poll(0)

    try:
        exited = actual_poll()
        exited.register(descriptor, select.POLLIN)
        assert exited.poll(30000), "known child did not exit"
        current = product._current(child.pid)
        assert current is not None and current[0] == "Z"
        identity = {"pid": child.pid, "start": current[19]}
        monkeypatch.setattr(
            product,
            "select",
            SimpleNamespace(
                poll=ObservedPoll, POLLIN=select.POLLIN, POLLHUP=select.POLLHUP
            ),
        )

        def observe():
            try:
                product._reaped(identity)
            except (AssertionError, OSError) as error:
                terminal.put(error)
                registered.put(("terminal", error))
            else:
                terminal.put(None)

        observer = threading.Thread(target=observe)
        observer.start()
        assert registered.get(timeout=30) == ("registered", select.POLLIN)
        assert registered.get(timeout=30) == ("registered", select.POLLHUP)
        assert terminal.empty(), "an exited, deliberately unreaped child is not reaped"
        child.wait(timeout=30)
        parent_reaped.set()
        assert terminal.get(timeout=30) is None
        observer.join(timeout=30)
        assert not observer.is_alive()
        assert product._current(child.pid) is None
    finally:
        child.wait(timeout=30)
        parent_reaped.set()
        os.close(descriptor)
        if observer is not None:
            observer.join(timeout=30)


@pytest.mark.skipif(not hasattr(os, "pidfd_open"), reason="Linux pidfd observation")
def test_missing_reap_event_never_proves_a_retained_worker_identity(monkeypatch):
    child = subprocess.Popen([sys.executable, "-c", "pass"])
    descriptor = os.pidfd_open(child.pid)
    try:
        exited = select.poll()
        exited.register(descriptor, select.POLLIN)
        assert exited.poll(30000)
        current = product._current(child.pid)
        assert current is not None and current[0] == "Z"
        identity = {"pid": child.pid, "start": current[19]}

        class NoReapEvent:
            def register(self, descriptor, events):
                assert events == select.POLLIN
                self.descriptor = descriptor
                self.events = events

            def modify(self, descriptor, events):
                assert descriptor == self.descriptor and events == select.POLLHUP
                self.events = events

            def poll(self, timeout):
                assert 0 <= timeout <= 30000
                return (
                    [(self.descriptor, select.POLLIN)]
                    if self.events == select.POLLIN
                    else []
                )

        monkeypatch.setattr(
            product,
            "select",
            SimpleNamespace(
                poll=NoReapEvent, POLLIN=select.POLLIN, POLLHUP=select.POLLHUP
            ),
        )
        with pytest.raises(AssertionError, match="Recorded worker is not reaped"):
            product._reaped(identity)
        assert product._current(child.pid)[19] == identity["start"]
    finally:
        child.wait(timeout=30)
        os.close(descriptor)
