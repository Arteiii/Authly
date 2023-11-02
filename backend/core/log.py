import sys
import datetime
import inspect

from colorama import init, Fore

init(autoreset=True)  # Initialize colorama


class Logger:
    @staticmethod
    def info(*args):
        if args:
            print(
                f"{Fore.BLUE}[INFO]    {args[0]}{Fore.RESET}"
            )  # Print the first string on the same line
            if len(args) > 1:  # Check if there are more than one string
                for i, msg in enumerate(
                    args[1:], start=1
                ):  # Print subsequent strings with indentation
                    print(
                        f"{Fore.BLUE}{'          ' * (10 if i == 1 else 14)}\
                            {msg}{Fore.RESET}"
                    )
        else:
            print(f"{Fore.BLUE}[INFO]    Info Log Message{Fore.RESET}")

    @staticmethod
    def warning(msg: str = "Warning Log Message"):
        print(f"{Fore.YELLOW}[WARNING]    {msg}{Fore.RESET}")

    @staticmethod
    def error(msg: str = "Error Log Message"):
        print(f"{Fore.RED}[ERROR]    {msg}{Fore.RESET}")

    @staticmethod
    def critical(*args):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        if args:
            print(
                f"{Fore.MAGENTA}|> --- [CRITICAL] -------- [\
{Fore.LIGHTMAGENTA_EX}{current_time}{Fore.RESET}{Fore.MAGENTA}]\
--- [{Fore.BLACK}{caller_info.filename}{Fore.MAGENTA}] --- [{Fore.BLUE}\
{caller_info.function}{Fore.MAGENTA}] --- [{Fore.LIGHTYELLOW_EX}\
{caller_info.lineno}{Fore.MAGENTA}]"
            )

        for arg in args[0:]:
            print(f"{Fore.MAGENTA}|{Fore.RESET} " + arg)
        print(
            f"{Fore.MAGENTA}|> -----------------------------------------------\
{Fore.RESET}"
        )
        sys.exit(1)

    @staticmethod
    def debug(*args):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        if args:
            print(
                f"{Fore.CYAN}|> --- [DEBUG] -------- [{Fore.LIGHTMAGENTA_EX}\
{current_time}{Fore.RESET}{Fore.CYAN}]\
--- [{Fore.BLACK}{caller_info.filename}{Fore.CYAN}] --- [{Fore.BLUE}\
{caller_info.function}{Fore.CYAN}] --- [{Fore.LIGHTYELLOW_EX}\
{caller_info.lineno}{Fore.CYAN}]"
            )

        for arg in args[0:]:
            print(f"{Fore.CYAN}|{Fore.RESET} " + arg)
        print(
            f"{Fore.CYAN}| -----------------------------------------------\
{Fore.RESET}"
        )


# Example usage of the custom_logger function
Logger.debug(
    "This is the first line of the log.",
    "This is the second line of the log.",
    "This is the third line of the log.",
)
Logger.critical(
    "This is the first line of the log.",
    "This is the second line of the log.",
    "This is the third line of the log.",
)


# mongo schema:
# {
#   timestamp: Date, // Timestamp of the logged event
#   level: String, // Log level, e.g., INFO, DEBUG, ERROR, etc.
#   message: String, // Description of the logged event
#   metadata: Object // Additional metadata related to the event
# }
