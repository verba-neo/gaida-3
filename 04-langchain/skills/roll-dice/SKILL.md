---
name: roll-dice
description: Roll dice using a random number generator. Use when asked to roll a die (d6, d20, etc.), roll dice, or generate a random dice roll.
---

# Roll Dice Skill

## Instructions

1. Identify the number of sides `<sides>` requested by the user (e.g., 6 for d6, 20 for d20).
2. Execute the following unified Python command using the `execute_command` tool (works on Windows, Mac, and Linux):

```bash
uv run python -c "import random; print(random.randint(1, <sides>))"
```