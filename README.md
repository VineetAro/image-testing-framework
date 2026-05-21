👁️ VLM Automated Testing & Performance Benchmarking Framework

An automated, local regression and SLA benchmarking suite designed for Vision-Language Models (VLMs) running on localhost environments (powered by Ollama).

This framework automates the validation of local visual models (such as llava:7b), scoring their output descriptions, auditing confidence scores, logging inference latency, and running historical regression checks before deploying updates to production.


🚀 Architectural Evolution: Inversion of Control (IoC)

Previously, this framework relied on a monolithic, imperative script-runner (run_tests.py) that manually managed test loops, error handling, and state compilation.

The framework has been fully refactored to an Aspect-Oriented Pytest Architecture. By deferring execution and test state management to the Pytest native engine, we achieved strict Separation of Concerns:

    Declarative Test Files: Test scripts no longer contain try/except loops, file saving logic, or manual recording steps. They focus exclusively on input parameters and assertions.

    Dependency Injection (Fixtures): The OllamaClient connection lifecycle is abstracted out of test files. Handled via session-scoped singletons in conftest.py, network connections are instantiated exactly once per test run rather than inside an iterative loop.

    Out-of-Band Instrumentation (Hooks): System metric tracking, latency profiling, traceback capturing, and Markdown report synthesis are handled globally behind the scenes via Pytest engine lifecycles (pytest_runtest_makereport).


🚀 "Built as a self-learning project to explore modern AI-assisted testing concepts using local multimodal models such as `llava:7b`. 🚀

---

# 🚀 Key Features

* Local AI model testing using Ollama
* Automated image inference validation
* Keyword-based response verification
* Confidence score threshold checks
* Inference latency tracking
* Modular framework architecture
* Reusable validation utilities
* Dynamic image loading and preprocessing
* Structured Markdown reporting
* Pytest-based execution support

---

# 🏗️ Framework Architecture

The framework follows a modular layered design to separate responsibilities cleanly across configuration, API communication, validation logic, reporting, and automated test execution.

Key architectural concepts explored:

* Separation of Concerns
* Reusable framework utilities
* Centralized configuration management
* Declarative test design using Pytest
* Lightweight dependency injection via fixtures
* Automated report generation
* Local AI model validation workflows

---

# 📁 Project Directory Structure

```text
image-testing-framework/
│
├── config/                      # Framework Parameters
│   └── settings.py              # URLs, thresholds, and execution configs
│
├── test_images/                 # Local image asset repository
│   ├── cat.jpg
│   ├── dog.jpg
│   ├── ghibli.png
│   └── running_fire_hydrant.png
│
├── framework/                   # Core Framework Logic
│   ├── __init__.py
│   ├── client.py                # Ollama API communication layer
│   ├── image_loader.py          # Image loading & Base64 conversion
│   ├── validator.py             # Keyword & confidence validation
│   └── reporter.py              # Markdown report generation
│
├── tests/                       # Automated Test Layer
│   ├── conftest.py              # Fixtures & test lifecycle hooks
│   ├── test_suites.py           # Centralized test datasets
│   └── test_vision.py           # Vision model test cases
│
├── .gitignore
└── README.md
```

---

# 🛠️ Installation

## Prerequisites

* Python 3.10+
* Ollama installed locally

Install Ollama:

```bash
ollama run llava:7b
```

---

# 📦 Setup

Clone the repository:

```bash
git clone https://github.com/your-username/image-testing-framework.git

cd image-testing-framework
```

Install dependencies:

```bash
pip install pillow requests pytest
```

---

# ▶️ Running Tests

Execute the Pytest suite:

```bash
pytest -v -s
```

Or execute specific test modules:

```bash
pytest tests/test_vision.py -v -s
```

---

# 📊 Sample Report Output

```markdown
# VLM Test Execution Report

## Summary

- Total Tests Run: 3
- Passed: 3
- Failed: 0

---

## Test Details

### ✅ Cat Detection - PASS
- Total Time: 179.63 Seconds
- Image: cat.jpg
- Details: Passed confidence and keyword thresholds.

### ✅ Dog Detection - PASS
- Total Time: 217.82 Seconds
- Image: dog.jpg
- Details: Passed confidence and keyword thresholds.

### ✅ Image Detection - PASS
- Total Time: 158.02 Seconds
- Image: running_fire_hydrant.png
- Details: Passed confidence and keyword thresholds.
```

---

# 🧠 Concepts Explored

This project explores practical concepts related to:

* AI-assisted testing
* Vision-language model validation
* Prompt engineering
* API testing
* Modular framework design
* Local LLM workflows
* Response parsing and validation
* Automated reporting
* Pytest fixtures and hooks

---

# ⚠️ Current Limitations

* CPU-only inference can result in high response latency
* Validation is keyword-based and not semantic-aware
* Confidence scoring depends on model-generated outputs
* Local model quality varies by hardware capability

---

# 🔮 Future Improvements

* Async HTTP support using httpx
* Semantic similarity validation
* Historical trend tracking
* JSON schema enforcement
* GPU acceleration benchmarking
* CI/CD integration
* Multi-model comparison support
* Automated HTML reporting


---

# 👨‍💻 Author

Vineet Arora

QA Engineer transitioning into AI-assisted testing, automation framework development, and local LLM validation workflows.
0s)
