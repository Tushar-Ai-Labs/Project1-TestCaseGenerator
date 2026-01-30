# Findings

## Research
(Empty)

## Discoveries
- **North Star:** Test Case Generator AI app taking story/feature as input, generating test cases via LLM.
- **Integrations:** Local Ollama API (CodeLlama). No external keys needed.
- **Source of Truth:** User Input.
- **Delivery Payload:** Local Web Interface (Frontend + Backend).
- **Behavioral Rules:** Input -> LLM -> Test Cases.

## Constraints
- Must use local Ollama instance.
- Must result in a web interface.
