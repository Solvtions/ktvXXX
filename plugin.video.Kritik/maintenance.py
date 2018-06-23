import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import glob
import common as Common
import os

AddonTitle="[COLOR ghostwhite]IPTV Tools[/COLOR]"
thumbnailPath = xbmc.translatePath('special://userdata/Thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.Kritik')
ICON = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Kritik', 'icon.png'))
mediaPath = os.path.join(addonPath, 'resources/art')
databasePath = xbmc.translatePath('special://userdata/Database')
USERDATA = xbmc.translatePath('special://userdata/')
AddonData = xbmc.translatePath('special://userdata/addon_data')
MaintTitle="[COLOR white]Fab Maintenance[/COLOR]"
dp = xbmcgui.DialogProgress()
Windows = xbmc.translatePath('special://home')
WindowsCache = xbmc.translatePath('special://home')
OtherCache = xbmc.translatePath('special://home/temp')
dialog = xbmcgui.Dialog()

class Gui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.header = kwargs.get("header")
        self.content = kwargs.get("content")

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.content)

path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi	

def CheckUpdates():
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	xbmc.executebuiltin('UpdateAddonRepos()')
	xbmc.executebuiltin('UpdateLocalAddons()')
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	xbmc.executebuiltin('Notification(Ckecking...,[COLOR white]Checking for updates...[/COLOR],3000,special://home/addons/plugin.video.Kritik/icon.png)')

def clearCache():
    
    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("[COLOR white]Delete Kodi Cache Files[/COLOR]", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
							if (f == "xbmc.log" or f == "xbmc.old.log" or f =="kodi.log" or f == "kodi.old.log" or f == "spmc.log" or f == "spmc.old.log"): continue
							os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("[COLOR white]Delete Kodi Temp Files[/COLOR]", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno(MaintTitle,str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
                
    xbmc.executebuiltin("Container.Refresh")
    dialog = xbmcgui.Dialog()
    xbmc.executebuiltin('Notification(Clean,[COLOR white]Cache cleaned[/COLOR],2000,special://home/addons/plugin.video.Kritik/icon.png)')
    
def deleteThumbnails():
    
    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Cached Images", "This option deletes all cached images","Cached images are background artwork and poster images", "Are you sure you want to do this?"):
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
								pass
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
		os.unlink(text13)
    except OSError:
        pass
	xbmc.executebuiltin("Container.Refresh")
	xbmc.executebuiltin('Notification(Clean,[COLOR white]Thumbnails cleaned[/COLOR],2000,special://home/addons/plugin.video.Kritik/icon.png)')

#######################################################################
#						Delete Packages
#######################################################################

def purgePackages():
    
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    if dialog.yesno("[COLOR white]Delete Package Cache Files[/COLOR]", "%d packages found."%file_count, "Delete Them?"):  
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                dialog = xbmcgui.Dialog()
                xbmc.executebuiltin('Notification(Purged,[COLOR white]All packages purged[/COLOR],2000,special://home/addons/plugin.video.Kritik/icon.png)')
            else:
                dialog = xbmcgui.Dialog()
                xbmc.executebuiltin('Notification(Not Required,[COLOR white]No Packages to Purge[/COLOR],2000,special://home/addons/plugin.video.Kritik/icon.png)')
	xbmc.executebuiltin("Container.Refresh")

#######################################################################
#						Autoclean Function
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

def view_LastError():

	cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
	tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
	WindowsCache = xbmc.translatePath('special://home')
	found = 0
	get_log = 0

	if os.path.exists(tempPath):
		for root, dirs, files in os.walk(tempPath,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							THE_ERROR = "[COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/COLOR]\n\n" + checker + '\n'
						if found == 0:
							dialog.ok(MaintTitle,'[COLOR white]Great news! We did not find any errors in your log.[/COLOR]')
							sys.exit(1)
						else:
							c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
							Common.TextBoxesPlain("%s" % c)
							sys.exit(0)

	if os.path.exists(WindowsCache):
		for root, dirs, files in os.walk(WindowsCache,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							THE_ERROR = "[COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/COLOR]\n\n" + checker + '\n'
						if found == 0:
							dialog.ok(MaintTitle,'[COLOR white]Great news! We did not find any errors in your log.[/COLOR]')
							sys.exit(1)
						else:
							c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
							Common.TextBoxesPlain("%s" % c)
							sys.exit(0)
	if got_log == 0:
		dialog.ok(MaintTitle,'[COLOR white]Sorry we could not find a log file on your system[/COLOR]')

def viewErrors():

	cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
	tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
	WindowsCache = xbmc.translatePath('special://home')
	found = 0
	get_log = 0
	i = 0
	String = " "

	if os.path.exists(tempPath):
		for root, dirs, files in os.walk(tempPath,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							i = i + 1
							if i == 1:
								String = "[COLOR red]ERROR NUMBER " + str(i) + "[/COLOR]\n\n" + checker + '\n'
							else:
								String = String + "[COLOR red]ERROR NUMBER: " + str(i) + "[/COLOR]\n\n" + checker + '\n'

						if found == 0:
							dialog.ok(MaintTitle,'[COLOR white]Great news! We did not find any errors in your log.[/COLOR]')
							sys.exit(1)
						else:
							c=String.replace('NEW_L','\n').replace('NEW_R','\r')
							Common.TextBoxesPlain("%s" % c)
							sys.exit(0)

	if os.path.exists(WindowsCache):
		for root, dirs, files in os.walk(WindowsCache,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							i = i + 1
							if i == 1:
								String = "[COLOR red]ERROR NUMBER " + str(i) + "[/COLOR]\n\n" + checker + '\n'
							else:
								String = String + "[COLOR red]ERROR NUMBER " + str(i) + "[/COLOR]\n\n" + checker + '\n'

						if found == 0:
							dialog.ok(MaintTitle,'[COLOR white]Great news! We did not find any errors in your log.[/COLOR]')
							sys.exit(1)
						else:
							c=String.replace('NEW_L','\n').replace('NEW_R','\r')
							Common.TextBoxesPlain("%s" % c)
							sys.exit(0)
	if got_log == 0:
		dialog.ok(MaintTitle,'[COLOR white]Sorry we could not find a log file on your system[/COLOR]')

def viewLogFile():
	kodilog = xbmc.translatePath('special://logpath/kodi.log')
	spmclog = xbmc.translatePath('special://logpath/spmc.log')
	kodiold = xbmc.translatePath('special://logpath/kodi.old.log')
	spmcold = xbmc.translatePath('special://logpath/spmc.old.log')
				
	if os.path.exists(spmclog):
		if os.path.exists(spmclog) and os.path.exists(spmcold):
			choice = xbmcgui.Dialog().yesno(MaintTitle,"[COLOR white]Current & Old Log Detected on your system[/COLOR]","[COLOR white]Which log would you like to view?[/COLOR]","", yeslabel='OLD',nolabel='CURRENT')
			if choice == 0:
				f = open(spmclog,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - spmc.log" % msg)
			else:
				f = open(spmcold,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - spmc.old.log" % msg)
		else:
			f = open(spmclog,mode='r'); msg = f.read(); f.close()
			Common.TextBoxes("%s - spmc.log" % msg)
			
	if os.path.exists(kodilog):
		if os.path.exists(kodilog) and os.path.exists(kodiold):
			choice = xbmcgui.Dialog().yesno(MaintTitle,"Current & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='OLD',nolabel='CURRENT')
			if choice == 0:
				f = open(kodilog,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - kodi.log" % msg)
			else:
				f = open(kodiold,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - kodi.old.log" % msg)
		else:
			f = open(kodilog,mode='r'); msg = f.read(); f.close()
			Common.TextBoxes("%s - kodi.log" % msg)
			
	if os.path.isfile(kodilog) or os.path.isfile(spmclog):
		return True
	else:
		dialog.ok(MaintTitle,'Sorry, No log file was found.','','[COLOR yellow]Team TurnITdigital[/COLOR]')

def autocleannow():
    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
							if (f == "xbmc.log" or f == "xbmc.old.log" or f =="kodi.log" or f == "kodi.old.log" or f == "spmc.log" or f == "spmc.old.log"): continue
							os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
				
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log" or f == "spmc.log" or f == "spmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
        
    if os.path.exists(thumbnailPath)==True:  
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
								pass
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
		os.unlink(text13)
    except OSError:
        pass
		
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

    xbmc.executebuiltin('Notification(Clean,[COLOR white]All temporary data has been cleaned[/COLOR],2000,special://home/addons/plugin.video.Kritik/icon.png)')
    xbmc.executebuiltin("Container.Refresh")