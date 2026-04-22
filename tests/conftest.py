"""pytest configuration for approval tests.

Configures a non-interactive reporter: tests fail immediately with the
received output shown, rather than launching a GUI diff tool.

To approve a new or changed output:
    cp tests/<test_module>.<test_name>.received.txt \
       tests/<test_module>.<test_name>.approved.txt
"""
import approvaltests


class _FailReporter:
    """Fail the test and print received content without opening any GUI."""

    def report(self, received_path: str, approved_path: str) -> bool:
        with open(received_path) as f:
            received = f.read()
        raise AssertionError(
            f"\nNo approved file at:\n  {approved_path}\n\n"
            f"Received output:\n{received}\n"
            f"To approve:\n"
            f"  cp {received_path} \\\n"
            f"     {approved_path}"
        )


def pytest_configure(config):  # noqa: ARG001
    approvaltests.set_default_reporter(_FailReporter())
