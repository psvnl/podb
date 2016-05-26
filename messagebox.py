'''
POdB: A purchase order management system for small businesses 
Copyright (C) 2016  Paulo S. V. N. Leal

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.

Contact: paulosvnleal@gmail.com
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import resources_rc

def _get_basic_msg_box(title, text, buttons, info_text=None):
    msg_box = QMessageBox()
    icon = QIcon()
    icon.addPixmap(QPixmap(":/podbicon.png"))
    msg_box.setWindowIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    if info_text:
        msg_box.setInformativeText(info_text)
    msg_box.setStandardButtons(buttons)
    return msg_box

def execute_critical_msg_box(title, text, buttons, info_text=None):
    msg_box = _get_basic_msg_box(title, text, buttons, info_text)
    msg_box.setIcon(QMessageBox.Critical)
    result = msg_box.exec_()
    return result
    
def execute_warning_msg_box(title, text, buttons, info_text=None):
    msg_box = _get_basic_msg_box(title, text, buttons, info_text)
    msg_box.setIcon(QMessageBox.Warning)
    result = msg_box.exec_()
    return result

def execute_info_msg_box(title, text, buttons, info_text=None):
    msg_box = _get_basic_msg_box(title, text, buttons, info_text)
    msg_box.setIcon(QMessageBox.Information)
    result = msg_box.exec_()
    return result