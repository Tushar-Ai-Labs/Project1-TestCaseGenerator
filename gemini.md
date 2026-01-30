# Project Constitution (gemini.md)

## 1. Data Schemas
**Input Schema (User Request):**
```json
{
  "feature_description": "string" // The user story or feature description
}
```

**Output Schema (Test Cases):**
```json
{
  "test_cases": [
    {
      "id": "TC_001",
      "title": "Test Case Title",
      "description": "Brief description of the test",
      "preconditions": "List of preconditions",
      "steps": [
        "Step 1",
        "Step 2"
      ],
      "expected_result": "Expected outcome"
    }
  ]
}
```

## 2. Behavioral Rules
- **Core Function:** Generate comprehensive test cases from a given story/feature description.
- **LLM Engine:** Use local Ollama API (CodeLlama).
- **Tone/Style:** Professional, standard QA format.
- **Determinism:** Ensure structural consistency (always return JSON matching schema).

## 3. Architectural Invariants
- **Layer 1:** SOPs in `architecture/`
- **Layer 2:** Navigation (Backend API to route requests)
- **Layer 3:** Tools (Python scripts interacting with Ollama)
- `gemini.md` is law.
- Data-First Rule: Schema before Tools.
