# Renderer: table
**Case:** csv_string_to_pretty

## Input Params
```json
{
  "rows": "product_id,name,stock\nA123,Wireless Mouse,150\nB456,Mechanical Keyboard,75",
  "fmt": "pretty"
}
```

## Output
```
+------------+---------------------+-------+
| product_id |         name        | stock |
+------------+---------------------+-------+
|    A123    |    Wireless Mouse   |  150  |
|    B456    | Mechanical Keyboard |   75  |
+------------+---------------------+-------+
```

## Expectation
This parses a raw CSV string and formats it as a pretty table. Verify the headers are read from the first line and the data is correctly structured.

## LLM Review
**Result:** none
