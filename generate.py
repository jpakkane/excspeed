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

import os, sys, shutil

class GenerateCode:

    def __init__(self):
        self.cppdir = 'cpp'
        self.cdir = 'plainc'
        self.cpp_main = '''#include<cstdio>
#include<cstdlib>
#include<headers.h>

int main(int argc, char **argv) {
    int ok = 0;
    int fail = 0;
    srandom(42); // Must be deterministic and the same for C and C++
    const int rounds = 1000;
    for(int i=0; i<rounds; i++) {
    try {
        ok += func0();
    } catch(...) {
        fail++;
    }
    printf("OK: %d\\nFail: %d\\n", ok, fail);
    return 0;
}
'''
        self.cpp_mainfile = os.path.join(self.cppdir, 'main.cpp')

    def deltrees(self):
        if os.path.exists(self.cppdir):
            shutil.rmtree(self.cppdir)
        os.mkdir(self.cppdir)
        if os.path.exists(self.cdir):
            shutil.rmtree(self.cdir)
        os.mkdir(self.cdir)


    def run(self):
        self.deltrees()
        open(self.cpp_mainfile, 'w').write(self.cpp_main)

if __name__ == '__main__':
    g = GenerateCode()
    g.run()
