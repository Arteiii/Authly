import sys

from colorama import init, Fore

init(autoreset=True)  # Initialize colorama


class Logger:
    @staticmethod
    def info(msg: str = "Info Log Message"):
        print(f"{Fore.BLUE}[INFO]    {msg}{Fore.RESET}")

    @staticmethod
    def warning(msg: str = "Warning Log Message"):
        print(f"{Fore.YELLOW}[WARNING]    {msg}{Fore.RESET}")

    @staticmethod
    def error(msg: str = "Error Log Message"):
        print(f"{Fore.RED}[ERROR]    {msg}{Fore.RESET}")

    @staticmethod
    def critical(msg: str = "Critical Log Message"):
        print(f"{Fore.MAGENTA}[CRITICAL]    {msg}{Fore.RESET}")
        sys.exit(1)

    @staticmethod
    def debug(msg: str = "Debug Log Message"):
        print(f"{Fore.CYAN}[DEBUG]    {msg}{Fore.RESET}")


# mongo schema:
# {
#   timestamp: Date, // Timestamp of the logged event
#   level: String, // Log level, e.g., INFO, DEBUG, ERROR, etc.
#   message: String, // Description of the logged event
#   metadata: Object // Additional metadata related to the event
# }
