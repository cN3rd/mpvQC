#!/usr/sbin/env python3

# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import glob
import os
import shutil
import sys
from os import path
from typing import Tuple

import polib

# The languages to translate into
_LANGUAGES: Tuple[str] = ("de", "en")

_WORKFLOW = \
    """ Make sure the project has the following skeleton:
    
    root-dir
        -gui
            - <abc>.ui
            
    The "-p" (provide) flag will generate some files and the project structure will change to the following:
    
    root-dir
        -gui
            - <abc>.ui
        -locale
            - <locale>
                - LC_MESSAGES
                    - ui_trans.ts
        -src
            - generated
                - <abc>.py
    
    After that the "-f" (finish) flag will create the binaries:
    
    root-dir
        -gui
            - <abc>.ui
        -locale
            - <locale>
                - LC_MESSAGES
                    - ui_trans.ts
                    - ui_trans.qm
                    - ui_transmo.mo
                    - ui_transpo.po
        -src
            - generated
                - <abc>.py
    """

_HELP_TEXT = \
    """Use -help for getting a detailed explanation of this script.\n""" + \
    """Use -p flag for providing translation files.\n""" + \
    """Use -f flag for generating binaries from provided translation files."""

# The location of this python script
_THIS_SCRIPT_LOCATION = os.path.dirname(os.path.realpath(sys.argv[0]))

_TOOLS = (
    ("pyuic5", "Should be installed if qt designer is installed."),
    ("pylupdate5", "Should be installed if qt designer is installed."),
    ("lrelease", "Should be installed if qt designer is installed."),
    ("ts2po", "Github: https://github.com/translate/translate"),
)


def to_bash(message: str, lvl: int = 1):
    """
    Used for debugging and understanding the process.
    """

    if lvl == 0:
        pass
    elif lvl == 1:
        print(message)


class Directory:

    def __init__(self, script_location):
        self.script_location = script_location
        to_bash("This script location is: " + script_location, lvl=0)
        self.structure: Tuple[str] = ("locale", "{}", "LC_MESSAGES")
        self.src = os.path.join(self.script_location, "src")
        self.src_gui = os.path.join(self.src, "gui", "generated")
        to_bash("This src gui will be " + self.src_gui, lvl=0)
        self.locale_dirs = [os.path.join(self.script_location, *self.structure).format(l) for l in _LANGUAGES]
        to_bash("Locale directories will be ", lvl=0)
        for l in _LANGUAGES:
            to_bash("- " + l, lvl=1)

    def create_dirs(self):
        self.create_directory_locale()
        self.create_directory_gui_py_files()

    def create_directory_locale(self):
        for loc in self.locale_dirs:
            Directory.create_path_if_not_exists(loc)

    def create_directory_gui_py_files(self):
        Directory.create_path_if_not_exists(self.src_gui)
        Directory.create_file_if_not_exists(os.path.join(self.src_gui, "__init__.py"))

    @staticmethod
    def create_path_if_not_exists(new_path: str):
        if not path.isdir(new_path):
            to_bash("Create path " + new_path, lvl=1)
            os.makedirs(new_path)

    @staticmethod
    def create_file_if_not_exists(new_file: str):
        with open(r'{}'.format(new_file), 'a') as the_file:
            the_file.write("")


class Transformer:
    def __init__(self, directory: Directory):
        self.directory = directory
        self.py_gui_target = os.path.join(directory.src_gui, "{}")

    def ui_to_py(self):
        ui_files = glob.glob(os.path.join(self.directory.script_location, "gui", "*.ui"))

        for ui_file in ui_files:
            to_bash("Found ui file " + ui_file, lvl=1)
            _, _tail = os.path.split(ui_file)
            f_name = os.path.splitext(_tail)[0]
            os.system("pyuic5 {} -o {}.py".format(ui_file, self.py_gui_target.format(f_name)))

    def py_to_ts(self):
        py_files = [fn for fn in glob.iglob(os.path.join(self.directory.src, "**/*.py"), recursive=True)
                    if (not fn.endswith("__.py"))]
        for py_file in py_files:
            to_bash("Found py file " + py_file, lvl=1)

        for lang_dir in self.directory.locale_dirs:
            os.system("pylupdate5 {} -ts {}.ts".format(" ".join(py_files), os.path.join(lang_dir, "ui_trans")))

    def ts_to_qm(self):
        for lang_dir in self.directory.locale_dirs:
            new_file = os.path.join(lang_dir, "ui_trans")
            os.system("lrelease {}.ts -qm {}.qm".format(new_file, new_file))
            os.system("ts2po {}.ts {}po.po".format(new_file, new_file))
            po = polib.pofile('{}po.po'.format(new_file))
            po.save_as_mofile('{}mo.mo'.format(new_file))


def tools_available() -> bool:
    passed: bool = True

    for tool in _TOOLS:
        if shutil.which(tool[0]) is None:
            passed = False
            print("Tool '{}' is missing ...\n\t{}".format(*tool))

    return passed


if __name__ == "__main__":

    if tools_available():
        if len(sys.argv) > 1:
            job = sys.argv[1]

            if job == "-help":
                print(_WORKFLOW)
            elif job == "-p":
                d = Directory(_THIS_SCRIPT_LOCATION)
                d.create_dirs()

                t = Transformer(d)
                t.ui_to_py()
                t.py_to_ts()
            elif job == "-f":
                d = Directory(_THIS_SCRIPT_LOCATION)
                d.create_dirs()

                t = Transformer(d)
                t.ts_to_qm()
            else:
                print(_HELP_TEXT)
        else:
            print(_HELP_TEXT)