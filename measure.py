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
import time
import math

def sizeprint(fname):
    unstripsize = os.stat(fname).st_size
    subprocess.check_call(['strip', fname])
    stripsize = os.stat(fname).st_size
    print('Unstripped:', unstripsize)
    print('Stripped:', stripsize)

class Measure:
    def __init__(self):
        self.depths = (50, 100, 150, 200, 250, 300, 350, 400, 450, 500)
        self.errorrates = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.num_measurements = 5

    def run(self):
        results = []
        for depth in self.depths:
            currow = ''
            for errorrate in self.errorrates:
                w = self.measure(depth, errorrate)
                currow += w
            results.append(currow)
        return results

    def time_command(self, command):
        times = []
        for _ in range(self.num_measurements):
            starttime = time.time()
            subprocess.check_call(command)
            endtime = time.time()
            times.append(endtime - starttime)
        return min(times)

    def measure(self, depth, errorrate):
        g = generate.GenerateCode(depth, 100000, errorrate)
        g.run()
        if os.path.exists('buildc'):
            shutil.rmtree('buildc')
        if os.path.exists('buildcpp'):
            shutil.rmtree('buildcpp')
        mesonexe = shutil.which('meson')
        if mesonexe is None:
            mesonexe = shutil.which('meson.py')
        if mesonexe is None:
            mesonexe = '../meson/meson.py'
        subprocess.check_call([mesonexe, 'buildc', g.cdir])
        subprocess.check_call([mesonexe, 'buildcpp', g.cppdir])
        subprocess.check_call(['ninja', '-C', 'buildc'])
        subprocess.check_call(['ninja', '-C', 'buildcpp'])
        ctime = self.time_command(['buildc/cprog'])
        cpptime = self.time_command(['buildcpp/cppprog'])
        if ctime < cpptime:
            result = 'C'
        else:
            result = 'E'
        if math.fabs(ctime-cpptime)/min(ctime, cpptime) < 0.1:
            return result.lower()
        return result

def simple_measure():
    g = generate.GenerateCode(1000, 100000, 5)
    g.run()
    if os.path.exists('buildc'):
        shutil.rmtree('buildc')
    if os.path.exists('buildcpp'):
        shutil.rmtree('buildcpp')
    subprocess.check_call(['../meson/meson.py', 'buildc', g.cdir])
    subprocess.check_call(['../meson/meson.py', 'buildcpp', g.cppdir])
    print('Plain C')
    subprocess.check_call(['ninja', '-C', 'buildc'])
    print('C++')
    subprocess.check_call(['ninja', '-C', 'buildcpp'])
    print('\nC binary size')
    subprocess.check_call(['time', 'buildc/cprog'])
    print('\nC++ binary size')
    subprocess.check_call(['time', 'buildcpp/cppprog'])

def matrix_measure():
    m = Measure()
    mat = m.run()
    for line in mat:
        print(line)

if __name__ == '__main__':
    #simple_measure()
    matrix_measure()
