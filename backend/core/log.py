import sys
import json
import datetime
import inspect

from colorama import init, Fore

init(autoreset=True)  # Initialize colorama

application = "Authly"


def footer(COL: str = Fore.WHITE):
    print(f"{COL}|> " + "-" * 50 + f"{Fore.RESET}")


def banner(
    main_col: str,
    main_text: str,
    filename: str,
    function: str,
    line: int,
    time: str,
    application: str = application,
):
    print(
        f"{main_col}|> --- {Fore.LIGHTCYAN_EX}{application}{main_col}"
        f" ---- [{main_text}] ---- [{Fore.YELLOW}{time}{Fore.RESET}"
        f"{main_col}] --- [{Fore.BLACK}{filename}{main_col}] --- "
        f"[{Fore.BLUE}{function}{main_col}] --- "
        f"[{Fore.LIGHTYELLOW_EX}{line}{main_col}]"
    )


class Logger:
    @staticmethod
    def info(*args):
        NAME = "INFO"
        COL = Fore.BLUE
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        if args:
            banner(
                main_col=COL,
                main_text=NAME,
                filename=caller_info.filename,
                function=caller_info.function,
                line=caller_info.lineno,
                time=current_time,
            )
        for arg in args[0:]:
            print(f"{COL}|{Fore.RESET} " + str(arg))
        if len(args) > 1:
            footer(COL)

    @staticmethod
    def warning(*args):
        NAME = "WARNING"
        COL = Fore.YELLOW
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        if args:
            banner(
                main_col=COL,
                main_text=NAME,
                filename=caller_info.filename,
                function=caller_info.function,
                line=caller_info.lineno,
                time=current_time,
            )
        for arg in args[0:]:
            print(f"{COL}|{Fore.RESET} " + str(arg))
        if len(args) > 1:
            footer(COL)

    @staticmethod
    def error(*args):
        NAME = "ERROR"
        COL = Fore.MAGENTA
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        if args:
            banner(
                main_col=COL,
                main_text=NAME,
                filename=caller_info.filename,
                function=caller_info.function,
                line=caller_info.lineno,
                time=current_time,
            )

        for arg in args[0:]:
            print(f"{COL}|{Fore.RESET} " + str(arg))
        if len(args) > 1:
            footer(COL)

    @staticmethod
    def critical(*args):
        NAME = "CRITICAL"
        COL = Fore.RED
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        if args:
            banner(
                main_col=COL,
                main_text=NAME,
                filename=caller_info.filename,
                function=caller_info.function,
                line=caller_info.lineno,
                time=current_time,
            )
        for arg in args[0:]:
            print(f"{COL}|{Fore.RESET} " + str(arg))
        if len(args) > 1:
            footer(COL)
        sys.exit(1)

    @staticmethod
    def debug(*args):
        NAME = "DEBUG"
        COL = Fore.CYAN
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        if args:
            banner(
                main_col=COL,
                main_text=NAME,
                filename=caller_info.filename,
                function=caller_info.function,
                line=caller_info.lineno,
                time=current_time,
            )

        for arg in args[0:]:
            print(f"{COL}|{Fore.RESET} " + str(arg))
        if len(args) > 1:
            footer(COL)


# Example usage of the custom_logger function
if __name__ == "__main__":
    Logger.debug(
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.error(
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.warning(
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.info(
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
