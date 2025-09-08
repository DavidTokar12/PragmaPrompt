# Renderer: shot
**Case:** shot_with_thought

## Input Params
```json
{
  "user": "Write a short poem about the moon.",
  "thought": "The user wants a poem. I will think about themes like light, night, and loneliness. I will structure it in three short stanzas.",
  "output": "Silver orb in velvet night,\nA silent watchman, pure and bright,\nGuiding sailors with its light."
}
```

## Output
```
User: Write a short poem about the moon.

<THOUGHT>
The user wants a poem. I will think about themes like light, night, and loneliness. I will structure it in three short stanzas.
</THOUGHT>

<OUTPUT>
Silver orb in velvet night,
A silent watchman, pure and bright,
Guiding sailors with its light.
</OUTPUT>
```

## Expectation
This shot includes a 'Thought' block. Review its placement and formatting to ensure it clearly represents a step before the final output.

## LLM Review
**Result:** none
