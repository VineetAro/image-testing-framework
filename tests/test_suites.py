# Test cases: (image_file, question, expected_keywords, test_name)
CORE_VISION_TEST_CASES_ANIMALS=[("cat.jpg", "What animal is in this image?",
         ["cat", "feline", "kitten", "tabby"],
         "Cat Detection"),

        ("dog.jpg", "What animal is in this image?",
         ["dog", "canine", "puppy", "hound"],
         "Dog Detection")]

CORE_VISION_TEST_CASES_OBJECTS= [("running_fire_hydrant.png", "What is in this image?",
         ["water", "fire", "hydrant", "fire hydrant"],
         "Image Detection")]

CORE_TEXT_TEST_CASES= [
    ("Was bedeutet 'Fire Hydrant' auf deutsch?", ["Wasser", "Feuer", "Feuerlöscher", "Feuerlöschbrunnen", "Hydrant"], "test_fire_hydrant"),
    ("Was bedeutet 'Speed Limit' auf deutsch?", ["Schnell", "Fahren", "Geschwindigkeitsbegrenzung"], "test_speed_limit"),
    ("Was bedeutet 'Emergency Exit' auf deutsch?", ["Gebäuden", "Ausgang", "Notausgang"], "test_emergency_exit")
]

HISTORIC_BASELINES = {
"Cat Detection": {"status": "PASS", "max_allowed_time": 150.0},
"Dog Detection": {"status": "PASS", "max_allowed_time": 190.0},
"RUNNING FIRE HYDRANT":{"status": "PASS", "max_allowed_time": 200.0},
"test_fire_hydrant":{"status": "PASS", "max_allowed_time": 40.0},
"test_traffic_light":{"status": "PASS", "max_allowed_time": 40.0},
}
