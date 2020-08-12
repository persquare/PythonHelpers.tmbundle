# For python3 compatibility
# from plistlib import plistlib.dumps, plistlib.loads
#
# Also see zk://150320082100

import os
import subprocess
import plistlib
import glob

dialog = os.environ['DIALOG']

def _call_dialog(command, *args):
    """ Call the Textmate Dialog process

    command is the command to invoke.
    args are the strings to pass as arguments
    a dict representing the plist returned from DIALOG is returned

    """
    popen_args = [dialog, command]
    popen_args.extend(args)
    result = subprocess.check_output(popen_args)
    return result

def register_images(imgdir):
    imglist = glob.glob(imgdir+'/*.png')
    imgnames = [os.path.basename(img).rsplit('.', 1)[0] for img in imglist]
    for (name, img) in zip(imgnames, imglist):
        _call_dialog('images', '--register', plistlib.dumps({name:img}))
    return imgnames

def present_popup(suggestions, typed='', extra_word_chars='_'):
    """
    suggestions is a list of dicts with display, image, and insert keys, the latter two are optional.
    insert text will be appended **after** completion.
    """
    retval = _call_dialog('popup',
                          '--suggestions', plistlib.dumps(suggestions),
                          '--alreadyTyped', typed,
                          '--additionalWordCharacters', extra_word_chars)

def completion_popup(completions, typed='', extra_word_chars='_'):
    """completions is a list of strings"""
    entries = [{'display':s} for s in completions]
    retval = _call_dialog('popup',
                          '--suggestions', plistlib.dumps(entries),
                          '--alreadyTyped', typed,
                          '--additionalWordCharacters', extra_word_chars)

def present_menu(menu_items):
    selections = [{'title':item} for item in menu_items]
    result = _call_dialog('menu', '--items', plistlib.dumps(selections))
    if not result:
        return None
    result = plistlib.loads(result)
    item = result.get('title')
    idx = menu_items.index(item)
    return idx

def present_tooltip(text, is_html=False):
    _call_dialog('tooltip', '--html' if is_html else '--text', text)