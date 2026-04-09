Execute the test-plan skill exactly as specified in @agent/skills/test-plan.md.

Arguments provided: $ARGUMENTS

If fewer than two @file arguments were provided, respond with:
⚠️  /test-plan 缺少必要參數（需要兩個）。

正確語法：
  /test-plan @agent/artifacts/pm/{feature-name}.md @agent/artifacts/exec-plan/{feature-name}.md

請補上參數後重新執行。

Otherwise, read both referenced artifacts and generate the test plan document.
