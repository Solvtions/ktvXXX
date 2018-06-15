import menu, util, urllib
import xbmcplugin, xbmcaddon, xbmcgui


sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.efukt'
addon = xbmcaddon.Addon(id=ADDON_ID)
parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None

if mode==1: # trending menu
    util.addMenuItems(menu.trendingMenu)
if mode==2: # load a page and find the videos
    util.loadVideos(parameters)
elif mode==3: # load a video
    util.loadPage(parameters)
if mode==100: # play video
    # playMedia(title, thumbnail, link, mediaType='Video', library=True, title2="")
    util.playMedia(parameters['name'], parameters['icon'], parameters['url'])
else:
    util.addMenuItems(menu.efuktMenu)