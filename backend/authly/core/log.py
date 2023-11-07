import sys
import datetime
import inspect

from colorama import init, Fore

init(autoreset=True)  # Initialize colorama

application = "Authly"


def footer(COL: str = Fore.WHITE):
    print(f"{COL}|> " + "-" * 50 + f"{Fore.RESET}\n")


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


def format_value(value):
    value_upper = str(value).upper()
    if value_upper == "TRUE":
        return f"{Fore.GREEN}{value_upper}{Fore.RESET}"
    elif value_upper == "FALSE" or value_upper == "FAILED":
        return f"{Fore.RED}{value_upper}{Fore.RESET}"
    elif value_upper == "PASSED":
        return f"{Fore.GREEN}{value_upper}{Fore.RESET}"
    elif value_upper == "WARNING":
        return f"{Fore.YELLOW}{value_upper}{Fore.RESET}"
    else:
        return str(value)


class Logger:
    verbosity_level = "PRODUCTION"

    @staticmethod
    def set_verbosity_level(level):
        Logger.verbosity_level = level

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
            print(f"{COL}|{Fore.RESET}  {str(arg)}")
        if len(args) > 1:
            footer(COL)
        if len(args) <= 1:
            print("\n")

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
            print(f"{COL}|{Fore.RESET}  {str(arg)}")
        if len(args) > 1:
            footer(COL)
        if len(args) <= 1:
            print("\n")

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
            print(f"{COL}|{Fore.RESET}  {str(arg)}")
        if len(args) > 1:
            footer(COL)
        if len(args) <= 1:
            print("\n")

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
            print(f"{COL}|{Fore.RESET}  {str(arg)}")
        if len(args) > 1:
            footer(COL)
        if len(args) <= 1:
            print("\n")
        sys.exit(1)

    @staticmethod
    def debug(*args):
        if Logger.verbosity_level == "DEVELOPMENT":
            NAME = "DEBUG"
            COL = Fore.CYAN
            current_time = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
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

    def tests(*args, format=True):
        NAME = "TESTS"
        COL = Fore.WHITE
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

        if format and args and isinstance(args[0], dict):
            for key, value in args[0].items():
                if isinstance(value, list):
                    print(f"{COL}| {Fore.RESET}{key} Tests:")
                    for sublist in value:
                        max_item_length = max(
                            len(str(sublist[item])) for item in sublist
                        )
                        for item_key, item_value in sublist.items():
                            print(
                                f"{COL}|{Fore.RESET}   - \
{str(format_value(item_value)).ljust(max_item_length)}   \
{item_key.ljust(15)}"
                            )
                else:
                    print(f"{COL}| {Fore.RESET}{key}: {format_value(value)}")

        else:
            for arg in args[0:]:
                print(f"{COL}|{Fore.RESET}  {str(arg)}")

        if len(args) > 1 or (
            args and isinstance(args[0], dict) and len(args[0]) > 1
        ):
            footer(COL)

    @staticmethod
    def set_verbosity(verbosity):
        Logger.verbosity_level = verbosity


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
