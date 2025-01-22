
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

## Setup Instructions

### Prerequisites
- Python 3.8+
- Discord Developer Token
- `dotenv` package

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/TeamPicker-Bot.git
   cd TeamPicker-Bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file:
   ```
   DISCORD_BOT_TOKEN=<your-discord-bot-token>
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

### How to Add to Discord
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and copy the token.
3. Add the bot to a server using the OAuth2 URL with the necessary permissions.

### Uploading to GitHub
1. Initialize a Git repository in your project folder:
   ```bash
   git init
   ```
2. Add a `.gitignore` file to exclude sensitive files:
   ```
   echo .env > .gitignore
   echo __pycache__/ >> .gitignore
   ```
3. Stage and commit your files:
   ```bash
   git add .
   git commit -m "Initial commit for TeamPicker Bot"
   ```
4. Create a new repository on GitHub.
5. Link your local repository to GitHub:
   ```bash
   git remote add origin https://github.com/<your-username>/TeamPicker-Bot.git
   git branch -M main
   git push -u origin main
   ```

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contributions
Feel free to fork, modify, and contribute to this repository. Create a pull request for any improvements or fixes.

## Support
For any issues, please open an [issue](https://github.com/<your-username>/TeamPicker-Bot/issues) on GitHub.
