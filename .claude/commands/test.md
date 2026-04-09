Execute the test skill exactly as specified in @agent/skills/test.md.

Arguments provided: $ARGUMENTS

If no arguments were provided, respond with:
⚠️  /test 缺少必要參數。

正確語法：
  /test @agent/artifacts/test-plan/{feature-name}.md

目前可用的 test-plan artifacts：
(list files in agent/artifacts/test-plan/)

請補上參數後重新執行。

Otherwise, read the referenced test-plan artifact, generate test code, run the tests, and report results. Do not auto-fix failures.
