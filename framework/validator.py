import re


class ResponseChecker:



    def contains_any(self, response_text: str, keywords: list) -> bool:
        """
              Returns True if ANY keyword from the list appears in response.
              Case insensitive. Checks whole words only.
              """
        response_lower = response_text.lower()
        for word in keywords:
            # \b is word boundary - "cat" won't match "category"
            pattern = r'\b' + word.lower() + r'\b'
            if re.search(pattern, response_lower):
                return True

        return False
    def contains_all(self, response_text: str, keywords: list) -> bool:
        """
        Returns True if ALL keyword from the list appears in response.
        Case insensitive. Checks whole words only.
        """
        response_lower = response_text.lower()
        for word in keywords:
            # \b is word boundary - "cat" won't match "category"
            pattern = r'\b' + word.lower() + r'\b'
            if not re.search(pattern, response_lower):
                return False

        return True

    def score(self, probability:float, min_Score: float) -> bool:
        """
        check if probability score is greater then the minimum score.
        """
        return probability >= min_Score


    def is_negative(self, response: str) -> bool:
        """
                Did model say "I don't see X" or "No X present"?
                This catches false negatives - model saying NO when answer is YES.
                """
        negative_phrases = [
            "don't see", "do not see", "cannot see",
            "no cat", "no dog", "not present", "not visible",
            "cannot find", "there is no", "there are no"
        ]

        response_lower = response.lower()
        for phrase in negative_phrases:
            if phrase in response_lower:
                return True

        return False

    def check_regression(self, test_name:str,status:str, current_time:float, baseline_dict: dict)->str:
        """
        Compares the current run results to historical baselines.
        Returns a string detailing any regressions, or an empty string if clean.
        """

        if status is None:
            return""

        # Safe look up: Check if this test exists in our baseline configuration
        baseline = baseline_dict.get(test_name)
        if not baseline:
            return ""

        warnings = []
        max_allowed = baseline.get("max_allowed_time", 150.0)
        if current_time > max_allowed:
            warnings.append(f"SLA Warning: Speed regressed to {current_time:.2f}s (Max allowed: {max_allowed}s)")

        #Status / Accuracy RegressionCheck
        baseline_status = baseline.get("status", "PASS").upper()
        current_status = status.upper()
        # If historical status was PASS, but current status is FAIL, that's a major regression!
        if baseline_status == "PASS" and current_status != "PASS":
            warnings.append("Accuracy Warning: This test previously PASSED but has now failed/errored!")

        # Join warning messages with a clean separator
        return " | ".join(warnings) if warnings else ""


"""
# Self-test
checker = ResponseChecker()

# Test 1: Cat correctly identified
response = {"Description":"I can see an orange tabby cat sitting on a mat","Probability":0.85}
keywords = ["cat", "feline", "kitten", "tabby"]

print("Contains any cat keyword:", checker.contains_any(response.get("Description"), keywords))
print("Score:", checker.score(response.get("Probability"), 0.80))

# Test 2: "Cat" appearing in "category" should NOT match
response2 = {"Description":"The category of this image is outdoor","Probability":0.71}
print("\n'category' should not match 'cat':", checker.contains_any(response.get("Description"), ["cat"]))

# Test 3: Negative response detection
neg_response =  {"Description":"I don't see any cat in this image","Probability":0.71}
print("\nIs negative response:", checker.is_negative(neg_response.get("Description")))
"""