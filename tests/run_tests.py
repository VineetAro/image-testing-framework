from framework.client  import OllamaClient as oClient
from framework.image_loader import ImageLoader as imageLoader
from framework.validator import ResponseChecker as rChecker
from framework.reporter import TestReporter as rReporter


import time

from pathlib import Path
import test_suites
from tests import baselines

test_cases = test_suites.CORE_VISION_TEST_CASES_ANIMALS
baselines = baselines.HISTORIC_BASELINES

def run_tests():
    duration = 0.0
    #This finds the directory where run_tests.py is saved (the "tests" folder)
    script_dir = Path(__file__).resolve().parent

    #This goes up one level to the main project folder, then down into "test_images"
    project_root_images = script_dir.parent / "test_images"

    #Pass this automatic, absolute path into your image loader
    loader = imageLoader(project_root_images)

    reporter = rReporter()
    checker = rChecker()
    for image_file, question, keywords, test_name in test_cases:
        try:
            image_b64 = loader.load(image_file)
            model = oClient(model="llava:7b")
            start_time = time.time()
            response_data = model.call_image_model(image_b64, question)
            duration = time.time() - start_time
            print(response_data )
            if response_data:
                score = checker.score(response_data.get("Probability",0), 0.8)
                found = checker.contains_any(response_data.get("Description",""), keywords)
                if found and score:
                    print(f"{test_name} passed")
                    regression_warning=checker.check_regression(test_name,"PASS", duration,baselines)
                    reporter.record_result(test_name, duration, "PASS", image_file,
                                           "Model matched expected keywords and passed confidence thresholds.",regression_warning)

                else:
                    print(f"{test_name} failed")
                    regression_warning = checker.check_regression(test_name, "FAIL", duration, baselines)
                    reporter.record_result(test_name, duration, "FAIL", image_file,
                                           f"Expected keywords not found or confidence score too low. Model output: {response_data}",regression_warning)

            else:
                # This catches if the client returned None
                regression_warning = checker.check_regression(test_name, "FAIL", duration, baselines)
                print(f"{test_name} failed: Model returned no valid response data.")
                reporter.record_result(test_name, duration, "FAIL", image_file, "Model failed to return valid JSON.",regression_warning)

        except FileNotFoundError as e:
            print(f"RESULT: ⏭️  SKIPPED - {e}")
            regression_warning = checker.check_regression(test_name, "FAIL", duration, baselines)
            reporter.record_result(test_name, duration, "SKIPPED", image_file, str(e), regression_warning)

        except Exception as e:
            regression_warning = checker.check_regression(test_name, "FAIL", duration, baselines)
            print(f"RESULT: ❌ ERROR - {e}")
            reporter.record_result(test_name, duration, "ERROR", image_file, str(e), regression_warning)
    # At the very end of all tests, compile and save the markdown report!
    reporter.generate_markdown()

if __name__ == "__main__":
    run_tests()
