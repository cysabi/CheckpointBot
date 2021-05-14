"""Initializes the Google Sheets connector."""

import os
import logging

import gspread

from .worksheet import Worksheet, Responses


class Connector:
    """Google connector."""

    def __init__(self):
        try:
            self.service = gspread.service_account(filename='google.json')
        except FileNotFoundError:
            logging.error("google.json - file not found.")
            raise EnvironmentError
        else:

            self.gsheet = self.service.open_by_key(os.getenv("GSHEET"))
            self.whatis = Responses(self.gsheet, "Whatis")

        logging.debug("Loaded google.connector")


connector = Connector()
