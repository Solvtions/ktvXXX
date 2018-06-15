import sys, urllib, os
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.efukt'
addon=xbmcaddon.Addon(id=ADDON_ID)
home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))

# the main menu structure
efuktMenu=[
    {
        "title":"Latest Videos", 
        "url":"http://efukt.com/", 
        "mode":2, 
        "poster":"none",
        "icon":"default.jpg", 
        "fanart":"default.jpg",
        "type":"", 
        "plot":"",
        "isFolder":True,
    }, {
        "title":"Trending", 
        "url":"http://efukt.com/", 
        "mode":1, 
        "poster":"none",
        "icon":"default.jpg", 
        "fanart":"default.jpg",
        "type":"", 
        "plot":"",
        "isFolder":True,
    }, {
        "title":"EFUKT Favourites", 
        "url":"http://efukt.com/favorites/", 
        "mode":2, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'main-search.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "isFolder":True,
    }, {
        "title":"Random Video", 
        "url":"http://efukt.com/random.php", 
        "mode":3, 
        "poster":"none",
        "icon":"default.jpg", 
        "fanart":"default.jpg",
        "type":"", 
        "plot":"",
        "isFolder":False,
    }
]

""", {
        "title":"Categories", 
        "url":"http://efukt.com/today/", 
        "mode":4, 
        "poster":"none",
        "icon":"default.jpg", 
        "fanart":"default.jpg",
        "type":"", 
        "plot":"",
        "isFolder":True,
    }, {
        "title":"Search", 
        "url":"http://efukt.com/search/", 
        "mode":5, 
        "poster":"none",
        "icon":"default.jpg", 
        "fanart":"default.jpg",
        "type":"", 
        "plot":"",
        "isFolder":True,
    },"""

trendingMenu=[
    {
        "title":"Trending Today", 
        "url":"http://efukt.com/today/", 
        "mode":2, 
        "poster":"none",
        "icon":"default.jpg", 
        "fanart":"default.jpg",
        "type":"", 
        "plot":"",
        "isFolder":True,
    }, {
        "title":"Trending this Month", 
        "url":"http://efukt.com/month/", 
        "mode":2, 
        "poster":"none",
        "icon":"default.jpg", 
        "fanart":"default.jpg",
        "type":"", 
        "plot":"",
        "isFolder":True,
    }, {
        "title":"Trending this Year", 
        "url":"http://efukt.com/year/", 
        "mode":2, 
        "poster":"none",
        "icon":"default.jpg", 
        "fanart":"default.jpg",
        "type":"", 
        "plot":"",
        "isFolder":True,
    }, {
        "title":"All Time Trenders", 
        "url":"http://efukt.com/all-time/", 
        "mode":2, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'main-search.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "isFolder":True,
    }
]