import sys
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

thisAddon = xbmcaddon.Addon(id='plugin.video.eroticshark')
thisAddonDir = xbmc.translatePath(thisAddon.getAddonInfo('path')).decode('utf-8')

if sys.platform == 'win32':
    imageDir = thisAddonDir + '\\resources\\image\\'
else:
    imageDir = thisAddonDir + '/resources/image/'

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def viewmode():
    addon_settings = xbmcaddon.Addon(id='plugin.video.eroticshark')
    dview = int(addon_settings.getSetting('dview'))

    if dview == 0:
        xbmc.executebuiltin('Container.SetViewMode(50)')
    elif dview == 1:
        xbmc.executebuiltin('Container.SetViewMode(500)')

    return

def build_supported_sites_directorys():
    url = build_url({'mode': 'alpha', 'func':'main_directorys', 'foldername': 'AlphaPorno'})
    li = xbmcgui.ListItem('AlphaPorno', iconImage=imageDir + 'alpha.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'befuck', 'func':'main_directorys', 'foldername': 'BeFUCK'})
    li = xbmcgui.ListItem('BeFUCK', iconImage=imageDir + 'befuck.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'croco', 'func':'main_directorys', 'foldername': 'CrocoTube'})
    li = xbmcgui.ListItem('CrocoTube', iconImage=imageDir + 'croco.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'drtuber', 'func':'main_directorys', 'foldername': 'Drtuber'})
    li = xbmcgui.ListItem('DrTuber', iconImage=imageDir + 'drtuber.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'eporner', 'func':'main_directorys', 'foldername': 'Eporner'})
    li = xbmcgui.ListItem('Eporner', iconImage=imageDir + 'eporner.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'faapy', 'func':'main_directorys', 'foldername': 'Faapy'})
    li = xbmcgui.ListItem('Faapy', iconImage=imageDir + 'faapy.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'heavyr', 'func':'main_directorys', 'foldername': 'HEAVYR'})
    li = xbmcgui.ListItem('HEAVY-R', iconImage=imageDir + 'heavyr.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'hotshame', 'func':'main_directorys', 'foldername': 'Hotshame'})
    li = xbmcgui.ListItem('Hotshame', iconImage=imageDir + 'hotshame.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'madthumbs', 'func':'main_directorys', 'foldername': 'MadThumBS'})
    li = xbmcgui.ListItem('MadThumBS', iconImage=imageDir + 'madthumbs.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'naked', 'func':'main_directorys', 'foldername': 'NakedTube'})
    li = xbmcgui.ListItem('NakedTube', iconImage=imageDir + 'naked.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'pinkrod', 'func':'main_directorys', 'foldername': 'Pinkrod'})
    li = xbmcgui.ListItem('Pinkrod', iconImage=imageDir + 'pinkrod.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'porndoe', 'func':'main_directorys', 'foldername': 'PornDoe'})
    li = xbmcgui.ListItem('PornDoe', iconImage=imageDir + 'porndoe.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'pornhub', 'func':'main_directorys', 'foldername': 'Pornhub'})
    li = xbmcgui.ListItem('Pornhub', iconImage=imageDir + 'pornhub.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'pornicom', 'func':'main_directorys', 'foldername': 'PorniCom'})
    li = xbmcgui.ListItem('PorniCom', iconImage=imageDir + 'pornicom.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'pornoid', 'func':'main_directorys', 'foldername': 'PornoID'})
    li = xbmcgui.ListItem('PornoID', iconImage=imageDir + 'pornoid.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'pornworms', 'func':'main_directorys', 'foldername': 'PornWORMS'})
    li = xbmcgui.ListItem('PornWORMS', iconImage=imageDir + 'pornworms.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'redtube', 'func':'main_directorys', 'foldername': 'RedTube'})
    li = xbmcgui.ListItem('RedTube', iconImage=imageDir + 'redtube.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'tube8', 'func':'main_directorys', 'foldername': 'Tube8'})
    li = xbmcgui.ListItem('Tube8', iconImage=imageDir + 'tube8.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'tubewolf', 'func':'main_directorys', 'foldername': 'Tubewolf'})
    li = xbmcgui.ListItem('TubeWolf', iconImage=imageDir + 'tubewolf.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'xhamster', 'func':'main_directorys', 'foldername': 'xHamster'})
    li = xbmcgui.ListItem('xHamster', iconImage=imageDir + 'xhamster.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'xvideos', 'func':'main_directorys', 'foldername': 'Xvideos'})
    li = xbmcgui.ListItem('XVideos', iconImage=imageDir + 'xvideos.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'wankoz', 'func':'main_directorys', 'foldername': 'Wankoz'})
    li = xbmcgui.ListItem('Wankoz', iconImage=imageDir + 'wankoz.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
   
    viewmode()
    xbmcplugin.endOfDirectory(addon_handle)

    return
