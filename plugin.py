############################################
# Author: gloug

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################

import os
import shutil
import sys
import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon


def translate_path(path):
    return xbmcvfs.translatePath(path) if sys.version_info >= (3, 0, 0) else xbmc.translatePath(path).decode('utf-8')


# Init
kodi_addon = xbmcaddon.Addon()
addon_id = kodi_addon.getAddonInfo('id')
addon_name = kodi_addon.getAddonInfo('name')
addon = (kodi_addon, sys.argv)
artwork = translate_path(os.path.join('special://home', 'addons', addon_id, 'art/'))
fanart = artwork + 'fanart.jpg'
messages = translate_path(os.path.join('special://home', 'addons', addon_id, 'resources', 'messages/'))
execute = xbmc.executebuiltin
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
log_level = xbmc.LOGINFO if sys.version_info >= (3, 0, 0) else xbmc.LOGNOTICE

# Path
cache_path = os.path.join(translate_path('special://home'), 'cache')
temp_path = os.path.join(translate_path('special://home'), 'temp')

# List of actions
CLEAR_CACHE_ACTION = "Clear Cache"
ACTIONS = [
    CLEAR_CACHE_ACTION
]


def log(msg, level=log_level):
    name = str(addon_name) + ' NOTICE'
    # override message level to force logging when addon logging turned on
    # level = xbmc.LOGNOTICE
    level = xbmc.LOGINFO if sys.version_info >= (3,0,0) else xbmc.LOGNOTICE
    try:
        xbmc.log('%s: %s' % (name, msg), level)
    except Exception as e:
        try:
            xbmc.log('Logging Failure', level)
            log(str(e))
        except TypeError as e:
            log(str(e))  # just give up


def convert_size(size):
    err_defaults = (0, 'Unavailable', 'None', '0B', '0M', '0 MB Free', '0 MB Total', '0M Free', '0M Total')
    if size in err_defaults:
        return '0 B'
    import math
    labels = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    try:
        i = int(math.floor(math.log(int(size), 1000)))
    except Exception as e:
        log(str(e))
        i = int(0)
    s = round(int(size) / math.pow(1000, i), 2)
    return '%s %s' % (str(s), labels[i])


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, f))
    return total_size


def delete_cache(auto_clear=False):
    """
    Method to clear Kodi's cache

    :param auto_clear: don't ask for confirmation
    :type auto_clear: bool
    """
    cache_paths = [cache_path, temp_path]
    size_to_clear = 0
    for path in cache_paths:
        size_to_clear += get_size(path)

    if not auto_clear:
        if not xbmcgui.Dialog().yesno("Please Confirm", "Size of Cache: %s, clear ?" % convert_size(size_to_clear)):
        # if not xbmcgui.Dialog().yesno("Please Confirm",
        #                               "                        Please confirm that you wish to clear\n"+\
        #                               "                              your Kodi application cache!",
        #                               "Cancel", "Clear"):
            return

    if xbmc.getCondVisibility('system.platform.ATV2'):
        cache_paths.extend([os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other'),
                            os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')])
    file_types = ['log', 'db', 'dat', 'socket']
    # if kodi.get_setting('acdb') == 'true':
    #     file_types.remove('db')
    directories = ('temp', 'archive_cache')
    for directory in cache_paths:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for f in files:
                    try:
                        if f.split('.')[1] not in file_types:
                            os.unlink(os.path.join(root, f))
                    except OSError:
                        pass
                for d in dirs:
                    try:
                        if d not in directories:
                            shutil.rmtree(os.path.join(root, d))
                    except OSError:
                        pass
    if not auto_clear:
        size_to_clear = 0
        for path in cache_paths:
            size_to_clear += get_size(path)
        xbmcgui.Dialog().ok(addon_name, "Done Clearing Cache files. New size: %s" % convert_size(size_to_clear))
        xbmc.executebuiltin("Container.Refresh")


# main
action_idx = int(xbmcgui.Dialog().select("Select action", ACTIONS))
if -1 < action_idx < len(ACTIONS):
    action = ACTIONS[action_idx]
    if action == CLEAR_CACHE_ACTION:
        delete_cache()

exit()
