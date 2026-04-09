Execute the exec-plan skill exactly as specified in @agent/skills/exec-plan.md.

Arguments provided: $ARGUMENTS

If no arguments were provided, respond with:
⚠️  /exec-plan 缺少必要參數。

正確語法：
  /exec-plan @agent/artifacts/pm/{feature-name}.md

目前可用的 pm artifacts：
(list files in agent/artifacts/pm/, excluding the postponed/ subdirectory)

請補上參數後重新執行。

Otherwise, read the referenced PM artifact and proceed with the skill steps.
