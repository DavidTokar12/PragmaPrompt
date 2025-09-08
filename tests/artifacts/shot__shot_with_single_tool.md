# Renderer: shot
**Case:** shot_with_single_tool

## Input Params
```json
{
  "user": "Search for today's top finance news.",
  "tools": [
    {
      "name": "web_search",
      "rationale": "The user is asking for current news, so I need to use the web search tool.",
      "input": {
        "query": "top finance news today",
        "domain": "finance"
      },
      "output": {
        "url": "news.com/1",
        "title": "Market Hits New High",
        "snippet": "..."
      },
      "thought": null
    }
  ],
  "output": {
    "summary": "The market reached a new high today, driven by tech stocks."
  }
}
```

## Output
```
User: Search for today's top finance news.

<TOOL_CHAIN>
<TOOL_STEP>
<NAME>
web_search
</NAME>
<RATIONALE>
The user is asking for current news, so I need to use the web search tool.
</RATIONALE>
<INPUT>
{
  "query": "top finance news today",
  "domain": "finance"
}
</INPUT>
<OUTPUT>
{
  "url": "news.com/1",
  "title": "Market Hits New High",
  "snippet": "..."
}
</OUTPUT>
</TOOL_STEP>
</TOOL_CHAIN>

<OUTPUT>
{
  "summary": "The market reached a new high today, driven by tech stocks."
}
</OUTPUT>
```

## Expectation
This shot demonstrates a single tool call. Review the 'Tool call chain' formatting, especially indentation and the clarity of the rationale, input, and output.

## LLM Review
**Result:** none
