# SOP: Test Case Generation

## 1. Goal
Generate structured JSON test cases from a user-provided feature description using a local LLM.

## 2. Input
- **Source:** User (via Frontend -> Backend API)
- **Format:** String (Feature description/Story)
- **Example:** "Login page with email and password."

## 3. Process
1.  **Receive Input:** Backend receives text.
2.  **Prompt Engineering:** Wrap input in a strict system prompt enforcing JSON schema.
3.  **LLM Inference:** Call Ollama (`qwen3:4b`) via `tools/generator.py`.
4.  **Validation:** Ensure output is valid JSON and matches schema.
5.  **Fallback:** If JSON is invalid, retry once or return error.

## 4. Output
- **Format:** JSON
- **Schema:**
    ```json
    {
      "test_cases": [
        {
          "id": "TC_001",
          "title": "...",
          "steps": ["..."],
          "expected_result": "..."
        }
      ]
    }
    ```

## 5. Error Handling
- **LLM Timeout:** Return 503 Service Unavailable.
- **Invalid JSON:** Return 500 with "Failed to generate structured data."
