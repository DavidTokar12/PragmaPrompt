# Renderer: to_display_block
**Case:** json_object_input

## Input Params
```json
{
  "input": {
    "user": {
      "name": "test",
      "id": 1
    },
    "status": "active"
  }
}
```

## Output
```
{
  "user": {
    "name": "test",
    "id": 1
  },
  "status": "active"
}
```

## Expectation
A dictionary (JSON object) with a nested object should be serialized correctly.

## LLM Review
**Result:** none
