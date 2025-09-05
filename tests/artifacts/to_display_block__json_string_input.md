# Renderer: to_display_block
**Case:** json_string_input

## Input Params
```json
{
  "input": "{\"key\": \"value\", \"is_json\": true}"
}
```

## Output
```
{
  "key": "value",
  "is_json": true
}
```

## Expectation
A string containing valid JSON should be detected and pretty-printed.

## LLM Review
**Result:** none
