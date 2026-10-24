# Workspace Rules & Instructions

## Automated Decision Logging
Whenever a key decision is made regarding:
- Sampling selection (adding/removing entities)
- Choosing or discarding proxies
- Entity resolution judgments (e.g. parent vs subsidiary, active vs defunct)
- Methodological trade-offs (what is excluded from the scope)

The agent must automatically update [DECISIONS.md](file:///d:/Proiect%20Veridion/DECISIONS.md) following the schema defined in [.agents/skills/decision-logger/SKILL.md](file:///d:/Proiect%20Veridion/.agents/skills/decision-logger/SKILL.md).
Any discarded alternative must be clearly noted so it automatically populates the required **Cut List** for the final submission.
