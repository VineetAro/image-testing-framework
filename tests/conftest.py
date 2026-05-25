import pytest
from framework.reporter import TestReporter
from framework.client import OllamaClient
from config import settings
import gc


@pytest.fixture(scope="function")  # Changed to function scope to re-evaluate per test case
def vlm_client(request):
    """
    Dynamically routes to the correct Ollama model based on the test case parameters.
    """
    # Look at the filename currently executing (e.g., vision_test.py or text_test.py)
    test_file = request.node.fspath.basename if hasattr(request.node, "fspath") else ""

    # Check if 'image_file' is in the test's parametrized arguments
    if "vision" in test_file.lower():
        model_name = settings.VLM_MODEL_IMAGE  # Routes to "llava:7b"
    else:
        model_name = settings.VLM_MODEL_TEXT  # Routes to "ibm/granite4.1:8b"

    # Instantiate the client with the dynamically selected model
    client = OllamaClient(model=model_name)
    yield client

    # 🧼 Teardown Phase: Clear VRAM right after the test function finishes
    gc.collect()
    try:
        requests.post(
            f"{settings.OLLAMA_API_BASE_URL}/api/generate",
            json={"model": model_name, "keep_alive": 0},
            timeout=5
        )
    except Exception:
        pass

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
        test_name = item.nodeid  # Returns: "tests/text_test.py::TestTextModels::test_problem_detection[0]"
        duration = report.duration

        # Pull parameters dynamically out of Pytest's internal memory
        image_name = item.callspec.params.get("image_file", "Unknown") if hasattr(item, 'callspec') else "Unknown"
        reg_warn = getattr(item, "regression_warning", "")
        resp_data = getattr(item, "response_data", "No response data captured")
        if report.passed:
            pytest.shared_reporter.record_result(
                test_name=test_name, total_time=duration, status="PASS",
                image_name=image_name, details="Passed confidence and keyword thresholds.",
                regression_warning=reg_warn,response=resp_data
            )
        elif report.failed:
            # Extract the failure message without crashing the framework
            error_msg = str(report.longrepr).split('\n')[-1]
            pytest.shared_reporter.record_result(
                test_name=test_name, total_time=duration, status="FAIL",
                image_name=image_name, details=error_msg,
                regression_warning=reg_warn,
                response=resp_data
            )