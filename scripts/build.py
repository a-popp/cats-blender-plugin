# MIT License
#
# Copyright (c) 2017 GiveMeAllYourCats
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Validate the manifest and rebuild the extension zip package.

Usage:
    python scripts/build.py
    python scripts/build.py --blender "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    python scripts/build.py --skip-validate --verbose

The zip is built in a temporary directory outside the source tree and then
moved into the output directory. Blender packages every file under
--source-dir, so building straight into build/ would package the previous
zip into the new one.
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO_ROOT, 'blender_manifest.toml')


def find_blender(explicit=None):
    if explicit:
        return explicit if os.path.isfile(explicit) else None

    env_blender = os.environ.get('BLENDER')
    if env_blender and os.path.isfile(env_blender):
        return env_blender

    on_path = shutil.which('blender')
    if on_path:
        return on_path

    found = []
    for pattern in (
        'C:/Program Files/Blender Foundation/Blender */blender.exe',
        '/Applications/Blender.app/Contents/MacOS/Blender',
        '/usr/local/bin/blender',
        '/opt/blender/blender',
    ):
        found.extend(glob.glob(pattern))
    # Version directories sort lexicographically, so the last entry is the
    # newest install.
    return sorted(found)[-1] if found else None


def run(cmd, verbose):
    print('$ ' + ' '.join(cmd))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace')
    output = (proc.stdout or '').rstrip()
    if verbose or proc.returncode != 0:
        print(output)
    return proc.returncode


def main():
    parser = argparse.ArgumentParser(description='Validate the manifest and rebuild the extension zip package.')
    parser.add_argument('--blender', help='Path to the Blender executable. Defaults to the BLENDER environment '
                                          'variable, then PATH, then common install locations.')
    parser.add_argument('--output-dir', default=os.path.join(REPO_ROOT, 'build'),
                        help='Directory to write the zip into (default: build/).')
    parser.add_argument('--skip-validate', action='store_true', help='Skip "extension validate".')
    parser.add_argument('--verbose', action='store_true', help='Show Blender output even when it succeeds.')
    args = parser.parse_args()

    if not os.path.isfile(MANIFEST):
        print('ERROR: blender_manifest.toml not found at ' + MANIFEST)
        return 1

    blender = find_blender(args.blender)
    if not blender:
        print('ERROR: Blender executable not found. Pass --blender <path> or set the BLENDER environment variable.')
        return 1
    print('Blender: ' + blender)

    if not args.skip_validate:
        if run([blender, '--background', '--factory-startup', '--command', 'extension', 'validate', REPO_ROOT],
               args.verbose) != 0:
            print('ERROR: extension validate failed.')
            return 1

    os.makedirs(args.output_dir, exist_ok=True)

    # The output directory usually lives inside the source tree (build/), and
    # Blender packages every file under --source-dir. Remove stale packages
    # first so a previous zip doesn't get nested into the new one.
    for stale in glob.glob(os.path.join(args.output_dir, '*.zip')):
        print('Removing stale ' + stale)
        os.remove(stale)

    with tempfile.TemporaryDirectory(prefix='cats-build-') as tmp_dir:
        if run([blender, '--background', '--factory-startup', '--command', 'extension', 'build',
                '--source-dir', REPO_ROOT, '--output-dir', tmp_dir], args.verbose) != 0:
            print('ERROR: extension build failed.')
            return 1

        zips = glob.glob(os.path.join(tmp_dir, '*.zip'))
        if not zips:
            print('ERROR: extension build produced no .zip in ' + tmp_dir)
            return 1

        for zip_path in zips:
            target = os.path.join(args.output_dir, os.path.basename(zip_path))
            if os.path.exists(target):
                os.remove(target)
            shutil.move(zip_path, target)
            print('Built {} ({:.1f} KB)'.format(target, os.path.getsize(target) / 1024.0))

    return 0


if __name__ == '__main__':
    sys.exit(main())
