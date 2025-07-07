# LLM Guidance

## Project File Structure

```
/Users/ktwu/Documents/quant101/1AI-polish/
├───.env_example
├───.gitignore
├───debug_env.py
├───LICENSE
├───project_info.sh
├───project_status.sh
├───README.CN.md
├───README.md
├───requirements_all.txt
├───requirements.txt
├───.git/...
├───app/
│   ├───__init__.py
│   ├───main_production.py
│   ├───main.py
│   ├───__pycache__/
│   ├───api/
│   │   ├───__init__.py
│   │   ├───__pycache__/
│   │   ├───dependencies/
│   │   │   └───__init__.py
│   │   └───v1/
│   │       ├───__init__.py
│   │       ├───endpoints.py
│   │       └───__pycache__/
│   ├───core/
│   │   ├───__init__.py
│   │   ├───config.py
│   │   └───__pycache__/
│   ├───models/
│   │   ├───__init__.py
│   │   ├───database.py
│   │   ├───schemas.py
│   │   └───__pycache__/
│   ├───services/
│   │   ├───__init__.py
│   │   ├───ai_processor.py
│   │   ├───celery_app.py
│   │   ├───deepseek_processor.py
│   │   └───__pycache__/
│   └───utils/
│       └───__init__.py
├───assets/
│   ├───Banner-AI-polish.png
│   ├───Screenshot-AI-polish-example.png
│   └───Screenshot-AI-polish.png
├───config/
├───docs/
│   └───index.html
├───fastapi_env/
│   ├───bin/...
│   ├───include/...
│   └───lib/...
├───logs/
└───tests/
    ├───__init__.py
    └───test_api.py
```

## Key Deployment Information (from README.md)

This project is named `1AI-polish`.

For more details, please refer to the main `README.md` and `README.CN.md` files.

## LLM-footprint-finding tools API Implementation Guidance

To implement an "LLM-footprint-finding tools API" within this project, you would generally follow these steps:

1.  **Define the API Endpoint:** Create a new endpoint in `app/api/v1/endpoints.py` that will expose the functionality. This endpoint would likely accept parameters such as a file path, a directory, or specific criteria for what constitutes an "LLM footprint" (e.g., specific keywords, patterns, or file types).

2.  **Develop the Core Logic:** In `app/services/`, create a new module (e.g., `llm_footprint_finder.py`) that encapsulates the logic for identifying LLM footprints. This module would use file system operations (reading files, listing directories) and potentially pattern matching or more advanced analysis to detect the desired "footprints."

3.  **Integrate with Existing Services:** If the footprint finding requires interaction with AI models (e.g., to analyze text for LLM-generated content), you might integrate with existing services like `ai_processor.py` or `deepseek_processor.py`.

4.  **Define Data Models:** If the API needs to return structured data (e.g., a list of files with detected footprints, or details about each footprint), define appropriate Pydantic schemas in `app/models/schemas.py`.

5.  **Add Dependencies:** If new external libraries are required for file parsing, pattern matching, or AI analysis, add them to `requirements.txt`.

6.  **Testing:** Create corresponding tests in `tests/test_api.py` (or a new test file like `tests/test_llm_footprint_finder.py`) to ensure the API and its underlying logic function correctly.

7.  **Configuration:** If there are configurable parameters for the footprint finding (e.g., thresholds, specific patterns), add them to `app/core/config.py`.

This approach ensures that the new functionality is well-integrated into the existing project structure, follows established patterns, and is maintainable.