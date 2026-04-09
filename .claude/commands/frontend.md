Execute the frontend skill exactly as specified in @agent/skills/frontend.md.

Arguments provided: $ARGUMENTS

If no arguments were provided, respond with:
⚠️  /frontend 缺少必要參數。

正確語法：
  /frontend @agent/artifacts/exec-plan/{feature-name}.md

目前可用的 exec-plan artifacts：
(list files in agent/artifacts/exec-plan/)

請補上參數後重新執行。

Otherwise, read the referenced exec-plan artifact, find the first incomplete front/* phase, and proceed with implementation.
