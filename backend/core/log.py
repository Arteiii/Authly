from colorama import init, Fore

init(autoreset=True)  # Initialize colorama


class Logger:
    @staticmethod
    def info(msg: str = "Info Log Message"):
        print(f"{Fore.BLUE}[INFO] {msg}{Fore.RESET}")

    @staticmethod
    def warning(msg: str = "Warning Log Message"):
        print(f"{Fore.YELLOW}[WARNING] {msg}{Fore.RESET}")

    @staticmethod
    def error(msg: str = "Error Log Message"):
        print(f"{Fore.RED}[ERROR] {msg}{Fore.RESET}")

    @staticmethod
    def critical(msg: str = "Critical Log Message"):
        print(f"{Fore.MAGENTA}[CRITICAL] {msg}{Fore.RESET}")

    @staticmethod
    def debug(msg: str = "Debug Log Message"):
        print(f"{Fore.CYAN}[DEBUG] {msg}{Fore.RESET}")


# Example usage:
# Logger.info("This is an information message.")
# Logger.warning("This is a warning message.")
# Logger.error("This is an error message.")
# Logger.critical("This is a critical message.")
