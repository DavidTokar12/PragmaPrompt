# Renderer: shot
**Case:** complex_tool_chain_shot

## Input Params
```json
{
  "title": "Example: Research and Summarize Financial Report",
  "context": {
    "username": "analyst_jane",
    "expertise_level": "expert"
  },
  "user": "Please find the latest quarterly earnings report for 'TechCorp' and provide a summary with key takeaways.",
  "tools": [
    {
      "name": "web_search",
      "rationale": "I need to find the official press release.",
      "input": {
        "query": "TechCorp latest quarterly earnings report",
        "domain": "finance"
      },
      "output": [
        {
          "url": "investors.techcorp.com/q3-2025-earnings",
          "title": "TechCorp Reports Q3 2025",
          "snippet": "..."
        }
      ],
      "thought": "The first result is the official source. I will use this."
    },
    {
      "name": "summarize_document",
      "rationale": "Now I will summarize the document to extract key points.",
      "input": {
        "url": "investors.techcorp.com/q3-2025-earnings"
      },
      "output": {
        "summary": "Strong earnings driven by cloud division.",
        "takeaways": [
          "Revenue hit $50B."
        ]
      },
      "thought": null
    }
  ],
  "thought": "The tool chain was successful. I will format the final answer.",
  "output": {
    "summary": "TechCorp reported record revenue of $50 billion in Q3 2025, fueled by its cloud services division.",
    "key_takeaways": [
      "Record Q3 revenue of $50 billion.",
      "Cloud division growth of 25% YoY."
    ],
    "confidence_score": 0.95
  }
}
```

## Output
```
### Example: Research and Summarize Financial Report

User: Please find the latest quarterly earnings report for 'TechCorp' and provide a summary with key takeaways.

<context>
{
  "username": "analyst_jane",
  "expertise_level": "expert"
}
</context>

<tool_chain>
<tool_step>
<name>web_search</name>
<rationale>I need to find the official press release.</rationale>
<input>
{
  "query": "TechCorp latest quarterly earnings report",
  "domain": "finance"
}
</input>
<output>
[
  {
    "url": "investors.techcorp.com/q3-2025-earnings",
    "title": "TechCorp Reports Q3 2025",
    "snippet": "..."
  }
]
</output>
<thought>The first result is the official source. I will use this.</thought>
</tool_step>
<tool_step>
<name>summarize_document</name>
<rationale>Now I will summarize the document to extract key points.</rationale>
<input>
{
  "url": "investors.techcorp.com/q3-2025-earnings"
}
</input>
<output>
{
  "summary": "Strong earnings driven by cloud division.",
  "takeaways": [
    "Revenue hit $50B."
  ]
}
</output>
</tool_step>
</tool_chain>

<thought>The tool chain was successful. I will format the final answer.</thought>

<output>
{
  "summary": "TechCorp reported record revenue of $50 billion in Q3 2025, fueled by its cloud services division.",
  "key_takeaways": [
    "Record Q3 revenue of $50 billion.",
    "Cloud division growth of 25% YoY."
  ],
  "confidence_score": 0.95
}
</output>
```

## Expectation
This is a complex shot with all possible components. Review the overall structure, formatting, and readability. Pay close attention to how all the different blocks (context, tools, thought, output) work together.

## LLM Review
**Result:** none
