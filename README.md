# TeamPicker Bot

TeamPicker Bot is a Discord bot that helps divide participants into balanced teams based on their skill levels. It supports grouping, reshuffling, and dynamically managing participants. The bot is perfect for organizing games, competitions, or collaborative events.

## Features
- Create teams based on specified `team_size` or `num_teams`.
- Add skill levels to participants (default skill level: 3).
- Handle group assignments to keep members together.
- Load participants and their skill levels from a `.txt` file.
- Save and manage participants dynamically.
- Clear all names, skills, and teams.

## Commands

### Team Management
- **`>shuffle`**
  - Create balanced teams.
  - Usage:
    - `>shuffle team_size=<size> names=<name_list>`
    - `>shuffle num_teams=<number> names=<name_list>`
    - Example: `>shuffle team_size=3 names=Alice,Bob,Charlie`
  - Group Players.
  - Usage:
    - `>shuffle num_teams=<number> names=<name_list> group=<name_list>`
    - `>shuffle num_teams=<number> names=<name_list> group=<name_list>;<name_list>`
    - Example: `>shuffle team_size=2 names=Alice,Bob,Charlie,Nathan group=Alice,Bob;Charlie,Nathan`
               `>shuffle team_size=2 names=Alice,Bob,Charlie,Nathan group=Alice,Bob`
  - Reshuffle from existing list of names.
  - Usage:
    - `>shuffle num_teams=<number>`
    - Example: `>shuffle num_teams=2`

- **`>clear`**
  - Clear all names, skill levels, and teams.
  - Usage: `>clear`

- **`>load`**
  - Load names and optional skill levels from a `.txt` file.
  - Attach a `.txt` file where each line is formatted as `Name [Skill Level]`.
  - Example file content:
    ```
    Alice 4
    Bob
    Charlie 2
    ```
  - Usage: `>load` (with file attachment).

- **`>teams`**
  - Display the current teams.
  - Usage: `>teams`

- **`>add`**
  - Add a person to the list of names with a default skill level.
  - Usage: `>add <name>`
  - Example: `>add Alice`

- **`>addSkill`**
  - Add a person to the list of names with a specific skill level (1-5).
  - Usage: `>addSkill name=<name> skill=<level>`
  - Example: `>addSkill name=Alice skill=4`

- **`>changeSkill`**
  - Update the skill level of an existing participant.
  - Usage: `>changeSkill name=<name> skill=<level>`
  - Example: `>changeSkill name=Alice skill=5`

- **`>viewSkill`**
  - Display the skill levels of all participants.
  - Usage: `>viewSkill`

- **`>remove`**
  - Remove a participant from the list of names.
  - Usage: `>remove <name>`
  - Example: `>remove Alice`

- **`>switch`**
  - Switch two participants between teams.
  - Usage: `>switch <name1> <name2>`
  - Example: `>switch Alice Bob`
