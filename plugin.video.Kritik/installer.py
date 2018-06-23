import xbmc,xbmcgui,os,sys,downloader

AddonTitle="[COLOR white]IPTV[/COLOR]"
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
HOME         =  xbmc.translatePath('special://home/')

def INSTALLAPK(name,url,description):

	if xbmc.getCondVisibility('system.platform.android'):

		if "NULL" in url:
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle, '[COLOR white]Download not currently available[/COLOR]',' ',' ')
			sys.exit(1)
				
		path = xbmc.translatePath(os.path.join('/storage/emulated/0/Download',''))
		dp = xbmcgui.DialogProgress()
		dp.create(AddonTitle,"","",'APK: ' + name)
		lib=os.path.join(path, 'app.apk')
		downloader.download(url, lib, dp)
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle, "[COLOR white]Launching the installer[/COLOR]" , "[COLOR white]Follow the install process to complete.[/COLOR]")
		xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:' + lib + '")' )
	else:
		dialog = xbmcgui.Dialog()
		dialog.ok("[COLOR white]Non Android Device[/COLOR]" , " ","[COLOR white]                    This is made for Android devices only[/COLOR]"," ")