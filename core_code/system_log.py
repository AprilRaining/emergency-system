import logging

def print_log(message):
    FORMATTER = "%(asctime)s — %(levelname)s : %(message)s"
    LOG_FILE = "emergency_sys.log"
    logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, filemode='a', format=FORMATTER, encoding='utf-8')
    logging.exception(message)
    print("\033[91m {}\033[00m" .format("Warning: "+ message))

def warn(message):
    # print without logging
    print("\033[91m {}\033[00m" .format("Warning: "+ message))


