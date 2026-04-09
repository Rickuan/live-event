Execute the commit skill exactly as specified in @agent/skills/commit.md.

Arguments provided: $ARGUMENTS

If no arguments were provided, respond with:
⚠️  /commit 缺少必要參數。

正確語法：
  /commit @agent/artifacts/exec-plan/{feature-name}.md

目前可用的 exec-plan artifacts：
(list files in agent/artifacts/exec-plan/)

請補上參數後重新執行。

Otherwise, read the referenced exec-plan artifact, find completed but uncommitted tasks, check the 500-line limit, show the proposed commit message in English for review, and wait for confirmation before committing. Do not push.
