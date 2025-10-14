# Renderer: table
**Case:** dataframe_to_pretty

## Input Params
```json
{
  "rows": [
    {
      "product_id": "A123",
      "name": "Wireless Mouse",
      "stock": 150
    },
    {
      "product_id": "B456",
      "name": "Mechanical Keyboard",
      "stock": 75
    }
  ],
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
This converts a pandas-like DataFrame into a pretty-printed table. Verify the headers are taken from the DataFrame's columns and the data is correctly rendered.

## LLM Review
**Result:** none
