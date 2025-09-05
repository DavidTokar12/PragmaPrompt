# Renderer: shot
**Case:** shot_with_context_and_input

## Input Params
```json
{
  "user": "What's the outlook for this company?",
  "context": {
    "username": "investor_bob",
    "expertise_level": "beginner"
  },
  "input": {
    "company_ticker": "TCORP",
    "timeframe": "6 months"
  },
  "output": "The outlook is positive, but volatile."
}
```

## Output
```
User: What's the outlook for this company?

<context>
{
  "username": "investor_bob",
  "expertise_level": "beginner"
}
</context>

<input>
{
  "company_ticker": "TCORP",
  "timeframe": "6 months"
}
</input>

<output>The outlook is positive, but volatile.</output>
```

## Expectation
This shot includes a structured context and input. Review how these blocks are formatted and separated from the main user prompt and output.

## LLM Review
**Result:** none
