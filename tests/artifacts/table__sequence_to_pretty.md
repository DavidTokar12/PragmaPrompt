# Renderer: table
**Case:** sequence_to_pretty

## Input Params
```json
{
  "rows": [
    [
      "A123",
      "Wireless Mouse",
      150
    ],
    [
      "B456",
      "Mechanical Keyboard",
      75
    ]
  ],
  "headers": [
    "ID",
    "Product",
    "In Stock"
  ],
  "fmt": "pretty"
}
```

## Output
```
+------+---------------------+----------+
|  ID  |       Product       | In Stock |
+------+---------------------+----------+
| A123 |    Wireless Mouse   |   150    |
| B456 | Mechanical Keyboard |    75    |
+------+---------------------+----------+
```

## Expectation
This converts a list of sequences to a pretty-printed table using explicit headers. Verify the provided headers are used and the data is aligned.

## LLM Review
**Result:** none
