import os
import urllib2
import xbmcaddon
import xbmcgui

def download_video(videotitle, videourl):
    try:
        addon_settings = xbmcaddon.Addon(id='plugin.video.eroticshark')
        savefolder = addon_settings.getSetting('savefolder').decode('utf-8')
        
        if savefolder == 'No folder selected':
            xbmcgui.Dialog().ok('Download Error', 'You must select a download folder in addon settings!')
            return
        
        req = urllib2.Request(videourl, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
        url_handler = urllib2.urlopen(req)
        meta = url_handler.info()
        file_size = int(meta.getheaders("Content-Length")[0])

        videotitle = unicode(videotitle, errors='ignore')
        videotitle = videotitle.decode('string_escape')
        localfile = open(savefolder + videotitle, 'wb')
        file_size_dl = 0
        block_sz = 8192

        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Video Downloading...')
        while True:
            buffer = url_handler.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            localfile.write(buffer)
            status = int(file_size_dl * 100. / file_size)
            pDialog.update(status, videotitle, 'Video size: ' + str(int(file_size/1024/1024)) + ' MByte','Downloaded data: ' + str(int(file_size_dl/1024/1024)) + ' MByte')
        
            if pDialog.iscanceled():
                pDialog.close()
                localfile.close()
                url_handler.close()
                os.remove(savefolder + videotitle)
                return

        pDialog.close()
        localfile.close()
        url_handler.close()
        xbmcgui.Dialog().ok('Download Successful', videotitle)
    except:
        url_content = 'HIBA'
        addon = xbmcaddon.Addon(id='plugin.video.eroticshark')
        addonname = addon.getAddonInfo('name')
        line1 = 'Sorry! Cannot connect to Database server!'
        line2 = 'Please try again later!'
        xbmcgui.Dialog().ok(addonname, line1, line2)
        return url_content
    return
