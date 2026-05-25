# tests/test_vision.py

import pytest
import time
from pathlib import Path

from framework.image_loader import ImageLoader
from framework.validator import ResponseChecker
from config import settings
from tests.test_suites import CORE_VISION_TEST_CASES_ANIMALS, HISTORIC_BASELINES, CORE_VISION_TEST_CASES_OBJECTS

loader = ImageLoader(settings.IMAGE_DIR)
checker = ResponseChecker()


@pytest.mark.parametrize("image_file, question, keywords, test_name", CORE_VISION_TEST_CASES_ANIMALS)
def test_animal_detection(image_file, question, keywords, test_name, vlm_client,request):

    #load Image
    image_b64 = loader.load(image_file)


    # Execute inference
    start_time = time.time()
    response_data = vlm_client.call_image_model(image_b64,question)
    duration = time.time()-start_time

    #Check for complete failures first
    assert response_data is not None, "Model failed to return valid JSON."

    #Analyze Response
    score = checker.score(response_data.get("Probability", 0.0), settings.MINIMUM_CONFIDENCE_SCORE)
    found = checker.contains_any(response_data.get("Description", ""), keywords)

    #Calculate Regression (and attach it to 'request.node' so conftest.py can read it)
    status = "PASS" if (found and score) else "FAIL"
    regression_warning = checker.check_regression(test_name, status, duration, HISTORIC_BASELINES)
    request.node.regression_warning = regression_warning

    # Capture response
    request.node.response_data = f'Description: {response_data.get("Description", "")}, Probability: {response_data.get("Probability", 0.0)}'

    #Assertions (If these fail, conftest logs them as FAIL)
    assert score is True, f"Confidence score too low. Model output: {response_data}"
    assert found is True, f"Expected keywords not found. Model output: {response_data}"


@pytest.mark.parametrize("image_file, question, keywords, test_name", CORE_VISION_TEST_CASES_OBJECTS)
def test_problem_detection(image_file, question, keywords, test_name, vlm_client,request):

    #load Image
    image_b64 = loader.load(image_file)


    # Execute inference
    start_time = time.time()
    response_data = vlm_client.call_image_model(image_b64,question)
    duration = time.time()-start_time

    #Check for complete failures first
    assert response_data is not None, "Model failed to return valid JSON."

    #Analyze Response
    score = checker.score(response_data.get("Probability", 0.0), settings.MINIMUM_CONFIDENCE_SCORE)
    found = checker.contains_all(response_data.get("Description", ""), keywords)

    #Calculate Regression (and attach it to 'request.node' so conftest.py can read it)
    status = "PASS" if (found and score) else "FAIL"
    regression_warning = checker.check_regression(test_name, status, duration, HISTORIC_BASELINES)
    request.node.regression_warning = regression_warning

    # Capture response
    request.node.response_data = f'Description: {response_data.get("Description", "")}, Probability: {response_data.get("Probability", 0.0)}'

    #Assertions (If these fail, conftest logs them as FAIL)
    assert score is True, f"Confidence score too low. Model output: {response_data}"
    assert found is True, f"Expected keywords not found. Model output: {response_data}"




