# test_suite_1.py
import logging
import pytest


class TestClass:
    def test_case_1(self):
        logging.info("In test suite 1, test case 1")
        print("Test case 1")

    def test_case_2(self):
        logging.info("In test suite 1, test case 2")
