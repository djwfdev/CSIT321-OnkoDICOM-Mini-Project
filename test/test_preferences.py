import pytest
import os

from View.preferences import *


def test_home_address_fail():
    """
    Test to ensure that the getHomeAddress method
    only outputs the home directory of the user
    """
    test_path = os.getcwd()
    assert str(get_home_address()) != test_path


def test_get_home_address():
    """
    Test to ensure that getHomeAddress returns
    the home directory as per the os of the user
    (e.g. 'C:/Users/alex')
    """
    test_path = os.path.expanduser('~')
    assert str(get_home_address()) == test_path

    test_path = str(Path.home())
    assert str(get_home_address()) == test_path


def test_get_data_no_database():
    """
    Test to ensure that if the database isn't
    created that the method creates it and
    inserts default values into the database
    """
    """
    folder_path = os.path.join(os.path.expanduser('~'), '.OnkoMiniproject')
    database_path = os.path.join(os.path.expanduser('~'), '.OnkoMiniproject/Onko.db')
    os.remove(database_path)
    os.rmdir(folder_path)
    """
    """
    The code above is to ensure that the database 
    is wiped clean for unit testing to occur on a 
    host machine where the database already
    exists
    """
    assert get_data() == [(1500, 500)]
    # read the comments above before debugging


def test_insert_data_no_database():
    """
    test to make sure that if database doesn't exist
    that insertData creates it and inserts the data
    provided when calling the method
    """
    folder_path = os.path.join(os.path.expanduser('~'), '.OnkoMiniproject')
    database_path = os.path.join(os.path.expanduser('~'), '.OnkoMiniproject/Onko.db')
    os.remove(database_path)
    os.rmdir(folder_path)

    insert_data(1, 1)
    assert get_data() == [(1, 1)]


def test_database_create():
    """
    Recreate the database to ensure that
    it is being created properly with the
    method alone
    """
    folder_path = os.path.join(os.path.expanduser('~'), '.OnkoMiniproject')
    database_path = os.path.join(os.path.expanduser('~'), '.OnkoMiniproject/Onko.db')
    os.remove(database_path)
    os.rmdir(folder_path)
    database_create()


def test_get_data_exists():
    """
    Test to see if something exists within the database
    to make sure it is created properly
    """
    assert get_data() != [(0, 0)]


def test_get_data_default_values():
    """
    Test default values for the database to ensure it is
    created properly
    """
    assert get_data() == [(1500, 500)]


def test_get_data():
    """
    Test to see if the data within the database is changed based on insertData
    """
    insert_data(1, 1)
    assert get_data() == [(1, 1)]
