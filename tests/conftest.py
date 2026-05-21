import pytest
from framework.reporter import TestReporter
from framework.client import OllamaClient
from config import settings



@pytest.fixture(scope="session")
def vlm_client():
    # Instantiating the client exactly as you had it in your code
    client = OllamaClient(model=settings.VLM_MODEL_NAME)
    yield  client

@pytest.fixture(scope="session", autouse=True)
def reporter_manager():
    reporter = TestReporter()
    pytest.shared_reporter = reporter

    yield

    reporter.generate_markdown()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Intercepts the result of every single test execution to automate reporting."""
    # Before the test runs
    outcome = yield  # 2. The test executes right here!
    print(outcome)
    # After the test runs: Grab the result
    report = outcome.get_result()

    # We only care about the actual execution phase ("call")
    if report.when == "call":
        test_name = item.name
        duration = report.duration

        # Pull parameters dynamically out of Pytest's internal memory
        image_name = item.callspec.params.get("image_file", "Unknown") if hasattr(item, 'callspec') else "Unknown"
        reg_warn = getattr(item, "regression_warning", "")

        if report.passed:
            pytest.shared_reporter.record_result(
                test_name=test_name, total_time=duration, status="PASS",
                image_name=image_name, details="Passed confidence and keyword thresholds.",
                regression_warning=reg_warn
            )
        elif report.failed:
            # Extract the failure message without crashing the framework
            error_msg = str(report.longrepr).split('\n')[-1]
            pytest.shared_reporter.record_result(
                test_name=test_name, total_time=duration, status="FAIL",
                image_name=image_name, details=error_msg,
                regression_warning=reg_warn
            )