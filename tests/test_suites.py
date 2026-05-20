# Test cases: (image_file, question, expected_keywords, test_name)
CORE_VISION_TEST_CASES =[("cat.jpg", "What animal is in this image?",
         ["cat", "feline", "kitten", "tabby"],
         "Cat Detection"),

        ("testImage.png", "What animal is in this image?",
         ["dog", "canine", "puppy", "hound"],
         "Dog Detection")]