import os

import pytest

from Controller.setup import *


def test_log_setup():
    """
    Test to make sure that if the right
    parameters are met that 1 is returned
    """
    assert log_setup('OnkoLog.log') == 1



