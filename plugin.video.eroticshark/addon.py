import os
import sys
import urllib
import urllib2
import urlparse
import xbmcaddon
import xbmcgui
import xbmcplugin

thisAddon = xbmcaddon.Addon(id='plugin.video.eroticshark')
thisAddonDir = xbmc.translatePath(thisAddon.getAddonInfo('path')).decode('utf-8')
sys.path.append(os.path.join(thisAddonDir, 'resources', 'lib'))

def just_beta(file_host):
    addon = xbmcaddon.Addon(id='plugin.video.eroticshark')
    addonname = addon.getAddonInfo('name')
    line1 = 'Sorry! Something went wrong!'
    line2 = 'Please try again later!'
    xbmcgui.Dialog().ok(addonname, line1, line2)  
    return

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:

    import websites
    websites.build_supported_sites_directorys()

elif mode[0] == 'back':

    xbmc.executebuiltin('Action(ParentDir)')

else:
    func = args.get('func', None)
    name = args.get('foldername', None)
    title = args.get('title', None)
    image = args.get('folderimage', None)
    pagenum = args.get('pagenum', None)

    resolver = __import__(mode[0])
    thisFunction = getattr(resolver, func[0])

    if title is None:
        if pagenum is None:
            thisFunction()
        else:
            thisFunction(name[0], pagenum[0])
    else:
        thisFunction(name[0], title[0], image[0], 'False')
