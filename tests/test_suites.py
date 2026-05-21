# Test cases: (image_file, question, expected_keywords, test_name)
CORE_VISION_TEST_CASES_ANIMALS=[("cat.jpg", "What animal is in this image?",
         ["cat", "feline", "kitten", "tabby"],
         "Cat Detection"),

        ("dog.jpg", "What animal is in this image?",
         ["dog", "canine", "puppy", "hound"],
         "Dog Detection")]

CORE_VISION_TEST_CASES_OBJECTS= [("running_fire_hydrant.png", "What is in this image?",
         ["water", "fire", "hydrant"],
         "Image Detection")]


HISTORIC_BASELINES = {
"Cat Detection": {"status": "PASS", "max_allowed_time": 150.0},
"Dog Detection": {"status": "PASS", "max_allowed_time": 190.0},
"RUNNING FIRE HYDRANT":{"status": "PASS", "max_allowed_time": 200.0}
}
