# pages.py
import string

from injector import Module, Binder
from selenium import webdriver


class LoginPage:
    def __init__(self, vv: string):
        self.vv = vv

    def login(self, username, password):
        # Your login implementation using Selenium
        pass


class DIModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(LoginPage, to=LoginPage)
