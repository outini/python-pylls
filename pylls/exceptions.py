#
#    Cachet API python client and interface (python-pylls)
#
#    Copyright (C) 2017 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#
#    This file is part of python-pylls
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.


class UnsupportedOperation(RuntimeError):
    """Requested operation is not supported"""
    def __str__(self):
        return "Requested operation is not supported"