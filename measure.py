#!/usr/bin/env python3
#
# Copyright (C) 2016 Jussi Pakkanen.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of version 3, or (at your option) any later version,
# of the GNU General Public License as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import generate
import subprocess
import os, shutil

def sizeprint(fname):
    unstripsize = os.stat(fname).st_size
    subprocess.check_call(['strip', fname])
    stripsize = os.stat(fname).st_size
    print('Unstripped:', unstripsize)
    print('Stripped:', stripsize)

if __name__ == '__main__':
    g = generate.GenerateCode(1000, 10000)
    g.run()
    if os.path.exists('buildc'):
        shutil.rmtree('buildc')
    if os.path.exists('buildcpp'):
        shutil.rmtree('buildcpp')
    subprocess.check_call(['../meson/meson.py', 'buildc', g.cdir])
    subprocess.check_call(['../meson/meson.py', 'buildcpp', g.cppdir])
    subprocess.check_call(['ninja', '-C', 'buildc'])
    subprocess.check_call(['ninja', '-C', 'buildcpp'])
    print('Plain C')
    subprocess.check_call(['time', 'buildc/cprog'])
    print('C++')
    subprocess.check_call(['time', 'buildcpp/cppprog'])
    print('\nC binary size')
    sizeprint('buildc/cprog')
    print('\nC++ binary size')
    sizeprint('buildcpp/cppprog')
