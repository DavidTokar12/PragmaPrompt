# Renderer: table
**Case:** sequence_to_csv

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
  "fmt": "csv"
}
```

## Output
```
ID,Product,In Stock
A123,Wireless Mouse,150
B456,Mechanical Keyboard,75
```

## Expectation
This converts a list of sequences to CSV format using explicit headers. Verify the provided headers are used and the output is a valid CSV string.

## LLM Review
**Result:** none
