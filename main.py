"""The main file of the Onko mini project. Running this file executes the program"""

import logging
import sys
import PySide6
from Controller.controller import Controller
from Controller.setup import log_setup


if __name__ == "__main__":
    log_setup("OnkoLog.log")
    logging.info("Log Setup Success")
    # ROOT DIRECTORY SETUP (not used in code, but is nice to have)
    root_dir = sys.argv[0]
    logging.info("startup success")

    # GUI setup
    app = PySide6.QtWidgets.QApplication(sys.argv)
    main_controller = Controller(root_dir)
    logging.info("GUI init Successful")
    main_controller.show_window()

    # Run GUI
    logging.info("Excecuting GUI Thread")
    app.exec()

    # Code below will run when the GUI is closed

    logging.info("GUI exec Successful")
    logging.info("END SESSION \n\n")

    sys.exit()
