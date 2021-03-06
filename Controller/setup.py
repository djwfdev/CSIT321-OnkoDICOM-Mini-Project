"""Setup file. Contains the logging setupr for now, but should a
config file be implemented, it will be read here. This file is in
the controller folder to keep it out of the root directory,
despite being called by main.py"""

import logging


def log_setup(filename):
    """logging setup"""
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(filename=filename,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%m/%d/%Y %I:%M:%S %p")
    return 1
