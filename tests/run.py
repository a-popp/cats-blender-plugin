# MIT License

# Copyright (c) 2017 GiveMeAllYourCats

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import glob
import sys
import os
import tempfile
import itertools
from subprocess import Popen, PIPE
from optparse import OptionParser

try:
    from termcolor import colored
except ImportError:
    # Fallback for environments without termcolor
    def colored(text, color, attrs=None):
        return text


start_time = time.time()

parser = OptionParser()
parser.add_option('-b', '--blend', dest='blender_exec', help='sets the blender executable', metavar='BLENDER', default='blender')
parser.add_option('-t', '--test', dest='globber_test', help='sets the unit to test', metavar='TEST', default='*')
parser.add_option('-c', '--ci', dest='ci', help='is ci running this test?', metavar='CI', default=False)
parser.add_option('-v', '--verbose', dest='verbosity', help='verbosity unit tests', metavar='VERBOSE', default=False)

(options, args) = parser.parse_args()

ci = str(options.ci).lower() in ('1', 'true', 'yes')
blender_exec = options.blender_exec
globber_test = options.globber_test
verbosity = str(options.verbosity).lower() in ('1', 'true', 'yes')

scripts = 0
exit_code = 0
scripts_only_executed_once = ['syntax.test.py']
scripts_executed = []


def show_time(time):
    rounded = round(time)
    string = str(rounded)
    color = 'grey'

    if rounded > 0:
        color = 'green'

    if rounded > 10:
        color = 'yellow'

    if rounded > 20:
        color = 'red'

    return colored(string, color, attrs=['bold'])


spinner = itertools.cycle(['-', '/', '|', '\\'])


def exit_test():
    end_message = ' > '
    if exit_code != 0:
        end_message += 'Test ' + colored('FAILED', 'red', attrs=['bold'])
    else:
        end_message += 'Test ' + colored('PASSED', 'green', attrs=['bold'])
    end_message += ' in ' + str(round((time.time() - start_time))) + ' seconds'
    print(end_message)
    sys.exit(exit_code)


def print_output(raw, output):
    try:
        print(output)
    except UnicodeEncodeError:
        # Console encoding can't handle some characters (e.g. Japanese on
        # Windows cp1252). Replace unencodable characters instead of crashing.
        encoding = sys.stdout.encoding or 'utf-8'
        print(output.encode(encoding, errors='replace').decode(encoding, errors='replace'))


# Iterate over each *.test.py file in the 'tests' directory.
# Tests that need a .blend file use programmatically generated fixtures.
# Tests that don't need a blend file (syntax, registration) run without one.
test_files = sorted(glob.glob('./tests/' + globber_test + '.test.py'))
if not test_files:
    print('ERROR: No test files found matching pattern: ' + globber_test)
    sys.exit(1)

addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bootstrap = (
    "import sys, os, importlib.util; "
    "addon_dir=" + repr(addon_dir) + "; "
    "spec=importlib.util.spec_from_file_location('cats', addon_dir + os.sep + '__init__.py', submodule_search_locations=[addon_dir]); "
    "cats=importlib.util.module_from_spec(spec); "
    "sys.modules['cats']=cats; "
    "spec.loader.exec_module(cats); cats.register()"
)

for file in test_files:
    basename = os.path.basename(file)
    if basename in scripts_only_executed_once:
        if basename in scripts_executed:
            continue

    scripts_executed.append(basename)
    scripts += 1
    start_time_unit = time.time()

    # Tests that don't need a blend file run with --factory-startup only
    # Tests that generate their own fixtures do so inside the test script
    cmd = [blender_exec, '--factory-startup', '-noaudio', '-b', '--python-expr', bootstrap, '--python', file]
    if ci:
        p = Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        raw_output = stdout.decode('utf-8', errors='replace') + stderr.decode('utf-8', errors='replace')
    else:
        # Redirect to a temp file: polling without draining the pipes would
        # deadlock once Blender fills the OS pipe buffer.
        with tempfile.TemporaryFile() as tmp_out:
            p = Popen(cmd, shell=False, stdout=tmp_out, stderr=tmp_out)
            while p.poll() is None:
                sys.stdout.write('\r' + next(spinner) + ' running ' + basename + '...')
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            sys.stdout.flush()
            tmp_out.seek(0)
            raw_output = tmp_out.read().decode('utf-8', errors='replace')

    if verbosity:
        print_output(raw_output, raw_output)

    if p.returncode != 0:
        exit_code = 1
        if not verbosity:
            print_output(raw_output, raw_output)

    elapsed = round(time.time() - start_time_unit)
    status = colored('PASS', 'green', attrs=['bold']) if p.returncode == 0 else colored('FAIL', 'red', attrs=['bold'])
    print(' > ' + basename + ' ' + status + ' in ' + show_time(elapsed) + 's')

exit_test()
