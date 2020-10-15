# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2020-present lambda-isel (https://github.com/lambda-isel)

from os import mkdir
from os.path import join
from requests import get
from xbmc import log, LOGNOTICE, translatePath
from xbmcaddon import Addon

LOCATION_COUNT = 7
LOCATION_TYPES = ['file', 'text']
PLAYLIST = 'playlist.m3u'


def main():
    addon = Addon()
    id = addon.getAddonInfo('id')
    profile = translatePath(addon.getAddonInfo('profile'))
    playlist = join(profile, PLAYLIST)
    update_iptv = addon.getSetting('update_iptv') == 'true'
    locations = [
        location
        for type in LOCATION_TYPES
        for number in range(0, LOCATION_COUNT)
        for location in addon.getSetting('{}_{}'.format(type, number)).split(',')
        if location
    ]
    try:
        mkdir(profile)
    except OSError:
        pass
    with open(playlist, 'w') as file:
        for location in locations:
            try:
                if ':' in location:
                    list = get(location).text.encode('utf-8')
                else:
                    list = open(location).read()
                file.write(list)
                log('{}: OK {}'.format(id, location), LOGNOTICE)
            except Exception as e:
                log('{}: KO {}, {}'.format(id, location, e), LOGNOTICE)
    if update_iptv:
        iptvsimple = Addon('pvr.iptvsimple')
        if iptvsimple.getSetting('m3uPathType') != '0':
            iptvsimple.setSetting('m3uPathType', '0')
        iptvsimple.setSetting('m3uPath', playlist)


if __name__ == '__main__':
    main()
