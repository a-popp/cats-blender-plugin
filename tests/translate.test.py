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

# Offline translation test: verify dictionary loading and translation
# work without any network access.

import sys
import traceback

errors = []

try:
    import cats
    cats.register()
except Exception:
    traceback.print_exc()
    errors.append('Registration failed')

try:
    from cats.tools import translate as Translate

    # Verify dictionary was loaded
    if not Translate.dictionary:
        errors.append('Dictionary is empty - load_translations failed')
    else:
        print('Dictionary loaded with {} entries'.format(len(Translate.dictionary)))

    # Verify dict_found flag
    import cats.globs as globs
    if not globs.dict_found:
        errors.append('globs.dict_found is False - dictionary file not found')
    else:
        print('globs.dict_found is True')

    # Test translation of known terms from the offline dictionary.
    # The dictionary (resources/dictionary.json) maps Japanese bone/shapekey
    # names to English. We test:
    # 1. A real Japanese-to-English translation (頭 -> Head)
    # 2. English passthrough (no change, changed=False)
    # 3. A compound name containing a Japanese term (頭.L -> Head_L)
    test_cases = [
        # (input, expected_output, expected_changed)
        ('\u982d', 'Head', True),          # 頭 -> Head
        ('head', 'head', False),           # English passthrough
        ('Head', 'Head', False),           # English passthrough
        ('\u982d.L', 'Head_L', True),      # 頭.L -> Head_L (.L -> _L replacement)
        ('\u53e3', 'Mouth', True),         # 口 -> Mouth
        ('\u76ee', 'Eye', True),           # 目 -> Eye
    ]

    for input_text, expected_output, expected_changed in test_cases:
        result, changed = Translate.translate(input_text)
        print('translate({!r}) -> {!r} (changed={})'.format(input_text, result, changed))
        if result != expected_output:
            errors.append('translate({!r}) returned {!r}, expected {!r}'.format(input_text, result, expected_output))
        if changed != expected_changed:
            errors.append('translate({!r}) changed={}, expected {}'.format(input_text, changed, expected_changed))

    # Test fix_jp_chars
    # Half-width katakana テ (0xFF83) should become full-width テ (0x30C6)
    half_width = '\uff83'
    full_width = '\u30c6'
    fixed = Translate.fix_jp_chars(half_width)
    if fixed != full_width:
        errors.append('fix_jp_chars failed: expected {}, got {}'.format(repr(full_width), repr(fixed)))
    else:
        print('fix_jp_chars: half-width -> full-width OK')

    # Verify no network-related attributes exist
    if hasattr(Translate, 'dictionary_google'):
        errors.append('dictionary_google still exists in translate module')
    if hasattr(Translate, 'reset_google_dict'):
        errors.append('reset_google_dict still exists in translate module')
    if hasattr(Translate, 'save_google_dict'):
        errors.append('save_google_dict still exists in translate module')

    print('No network translation attributes found')

except Exception:
    traceback.print_exc()
    errors.append('Translation test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('TRANSLATE TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
