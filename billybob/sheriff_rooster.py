#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


class SheriffRooster:

    def __init__(self, keyfile=None, **kargs):
        if keyfile is None:
            self.keyfile = os.environ['GOOGLE_KEYFILE']
        else:
            self.keyfile = keyfile
        self.worksheet_name = 'ActiveEon Sheriff Roster'
        self.spreadsheet_name = 'Sheet1'
        if 'WORKSHEET_NAME' in kargs:
            self.worksheet_name = kargs['WORKSHEET_NAME']
        if 'SPREADSHEET_NAME' in kargs:
            self.spreadsheet_name = kargs['SPREADSHEET_NAME']
        scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.keyfile,
                                                                            scope)
        gc = gspread.authorize(self.credentials)
        self.sheet = gc.open(self.worksheet_name).worksheet(self.spreadsheet_name)

    def get_users(self):
        users = []
        users_name = [n for n in self.sheet.col_values('2') if n != '']
        for name in users_name:
            cell_name = self.sheet.find(name)
            cell_days = self.sheet.cell(cell_name.row, cell_name.col+1)
            users.append({'name': cell_name.value, 'days': int(cell_days.value)})
        return users
