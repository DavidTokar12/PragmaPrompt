# Renderer: table
**Case:** csv_string_to_csv

## Input Params
```json
{
  "rows": "product_id,name,stock\nA123,Wireless Mouse,150\nB456,Mechanical Keyboard,75",
  "fmt": "csv"
}
```

## Output
```
product_id,name,stock
A123,Wireless Mouse,150
B456,Mechanical Keyboard,75
```

## Expectation
This parses a raw CSV string and outputs it in standard CSV format. Verify the output is a valid, standard CSV string with a header row.

## LLM Review
**Result:** none
