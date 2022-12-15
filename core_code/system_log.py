import logging


def print_log(message):
    FORMATTER = "%(asctime)s — %(levelname)s : %(message)s"
    LOG_FILE = "emergency_sys.log"
    logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE,
                        filemode='a', format=FORMATTER, encoding='utf-8')
    logging.exception(message)
    print("\033[91m {}\033[00m".format("Warning: " + message))


def warn(message):
    # print without logging
    print("\033[91m {}\033[00m" .format("Warning: " + message))


def prGreen(message): print("\033[92m {}\033[00m" .format(message))


def prYellow(message): print("\033[93m {}\033[00m" .format(message))


def prLightPurple(message): print("\033[94m {}\033[00m" .format(message))


def prPurple(message): print("\033[95m {}\033[00m" .format(message))


def prCyan(message): print("\033[96m {}\033[00m" .format(message))


def prLightGray(message): print("\033[97m {}\033[00m" .format(message))


def prBlack(message): print("\033[98m {}\033[00m" .format(message))
