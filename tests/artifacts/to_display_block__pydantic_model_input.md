# Renderer: to_display_block
**Case:** pydantic_model_input

## Input Params
```json
{
  "input": {
    "name": "pydantic_obj",
    "value": 456
  }
}
```

## Output
```
{
  "name": "pydantic_obj",
  "value": 456
}
```

## Expectation
A Pydantic model instance should be serialized to pretty-printed JSON.

## LLM Review
**Result:** none
