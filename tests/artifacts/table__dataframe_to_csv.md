# Renderer: table
**Case:** dataframe_to_csv

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
This converts a pandas-like DataFrame into CSV format. Verify the headers are taken from the DataFrame's columns and the output is a valid CSV.

## LLM Review
**Result:** none
