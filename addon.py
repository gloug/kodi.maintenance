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

import datetime
import os
import shutil
import sys
import re
import traceback
import xbmc
import xbmcgui
from libs import kodi
from libs import viewsetter

# Init
addon_id = kodi.addon_id
addon = (addon_id, sys.argv)
AddonName = kodi.addon.getAddonInfo('name') + " for Kodi"
artwork = kodi.translate_path(os.path.join('special://home', 'addons', addon_id, 'art/'))
fanart = artwork + 'fanart.jpg'
messages = kodi.translate_path(os.path.join('special://home', 'addons', addon_id, 'resources', 'messages/'))
execute = xbmc.executebuiltin
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

# Path
cache_path = os.path.join(kodi.translate_path('special://home'), 'cache')
temp_path = os.path.join(kodi.translate_path('special://home'), 'temp')

# List of actions
CLEAR_CACHE_ACTION = "Clear Cache"
ACTIONS = [
    CLEAR_CACHE_ACTION
]


def delete_cache(auto_clear=False):
    """
    Method to clear Kodi's cache

    :param auto_clear: don't ask for confirmation
    :type auto_clear: bool
    """
    if not auto_clear:
        if not xbmcgui.Dialog().yesno("Please Confirm",
                                      "                        Please confirm that you wish to clear\n"+\
                                      "                              your Kodi application cache!",
                                      "Cancel", "Clear"):
            return
    cache_paths = [cache_path, temp_path]
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
        xbmcgui.Dialog().ok(AddonName, "Done Clearing Cache files")
        xbmc.executebuiltin("Container.Refresh")


action_idx = int(xbmcgui.Dialog().select("Select action", ACTIONS))
if -1 < action_idx < len(ACTIONS):
    action = ACTIONS[action_idx]
    if action == CLEAR_CACHE_ACTION:
        delete_cache()

exit()
