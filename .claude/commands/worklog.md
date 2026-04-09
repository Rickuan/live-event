Execute the worklog skill exactly as specified in @agent/skills/worklog.md.

No arguments needed. Proceed immediately:
1. Check agent/worklog/sessions/ for the most recent session file to determine the time range.
2. Run git log to get commits since the last session (or today if no prior session exists).
3. Scan agent/artifacts/exec-plan/*.md for [x] completed tasks not yet included in a session summary.
4. Generate a Chinese session summary and save it to agent/worklog/sessions/YYYY-MM-DD-HH-MM.md.
