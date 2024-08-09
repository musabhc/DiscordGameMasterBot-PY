# Discord GameMaster Bot

A Discord bot for managing interactive word games with various word packages. The bot allows users to view available word packages and start games where participants can join and receive words from the selected package.

## Features

- **Word Package Display**: Users can view available word packages.
- **Interactive Games**: Start a game where users can join, and a random word is assigned from the selected package.
- **Customizable Word Packages**: Easily add new word packages by placing text files in the specified directory.

## Requirements

- Python 3.8 or higher
- Discord.py library
- `python-dotenv` library for environment variables

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/musabhc/discord-gamemaster-bot.git
   cd discord-gamemaster-bot
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**<br>
   Create a .env file in the root directory and add your Discord bot token:
   ```bash
   DISCORD_TOKEN=your-discord-bot-token
   ```
4. **Add your word packages:**<br>
   Place your word packages as .txt files in the word-packages/ directory. Each line in the text file should contain one word.
5. **Run the bot:**
   ```bash
   python main.py
   ```
## Usage

- **Command to Start the Game**: `!wordGame`
- **View Word Packages**: Click the "Packages" button.
- **Start the Game**: Click the "Play" button and select a package.

## Project Structure

```plaintext
.
├── word-packages/          # Directory containing word package text files
├── functions/                 # Directory for command functions
│   ├── roll_dice.py
│   ├── countdown.py
│   └── word_game.py
├── main.py                    # Main entry point of the bot
├── .env                       # Environment variables file (not included in repo)
└── README.md                  # Project documentation
```
## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, feel free to reach out to me on [GitHub](https://github.com/musabhc).


