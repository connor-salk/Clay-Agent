# Summarize Clay Update

This prompt is reserved for a future prompt-driven refresh flow.

## Current Status

The current v1 refresh pipeline does not invoke this prompt. It uses heuristic summarization implemented in `src/clay_refresh.py` so the repo stays lightweight and runnable without model dependencies.

## Future Prompt Contract

When a future version wires this prompt into the refresh flow, it should read the latest Clay update and produce:

1. A short summary of what changed
2. The likely impact on sourcing, enrichment, or list-building workflows
3. Any new capability worth testing
4. Any limitation, ambiguity, or follow-up question to record

Keep the output concise and operational.
