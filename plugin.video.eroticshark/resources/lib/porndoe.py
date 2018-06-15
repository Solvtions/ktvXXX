import os
import sys
import urllib
import urllib2
import re
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

thisAddon = xbmcaddon.Addon(id='plugin.video.eroticshark')
thisAddonDir = xbmc.translatePath(thisAddon.getAddonInfo('path')).decode('utf-8')
sys.path.append(os.path.join(thisAddonDir, 'resources', 'lib'))

if sys.platform == 'win32':
    imageDir = thisAddonDir + '\\resources\\image\\'
    download_script = thisAddonDir + '\\resources\\lib\\porndoe.py'
else:
    imageDir = thisAddonDir + '/resources/image/'
    download_script = thisAddonDir + '/resources/lib/porndoe.py'

base_url = sys.argv[0]

if sys.argv[1] != 'DOWNLOAD':
    addon_handle = int(sys.argv[1])

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def find_read_error(top_url):
    try:
        req = urllib2.Request(top_url, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
        url_handler = urllib2.urlopen(req)
        url_content = url_handler.read()
        url_handler.close()
    except urllib2.HTTPError as e:
        if e.code == 404:
            no_video('')
            xbmcplugin.endOfDirectory(addon_handle)
            return 'HIBA'
    except:
        url_content = 'HIBA'
        addon = xbmcaddon.Addon(id='plugin.video.eroticshark')
        addonname = addon.getAddonInfo('name')
        line1 = 'Sorry! Cannot connect to Database server!'
        line2 = 'Please try again later!'
        xbmcgui.Dialog().ok(addonname, line1, line2)
        return url_content
    return url_content

def just_beta(file_host):
    addon = xbmcaddon.Addon(id='plugin.video.eroticshark')
    addonname = addon.getAddonInfo('name')
    line1 = 'Sorry! Something went wrong!'
    line2 = 'Please try again later!'
    xbmcgui.Dialog().ok(addonname, line1, line2)  
    return

def just_removed(file_host):
    addon = xbmcaddon.Addon(id='plugin.video.eroticshark')
    addonname = addon.getAddonInfo('name')
    line1 = 'Sorry! Cannot connect to Database server!'
    line2 = 'Please try again later!'
    xbmcgui.Dialog().ok(addonname, line1, line2)  
    return

def no_video(file_host):
    addon = xbmcaddon.Addon(id='plugin.video.eroticshark')
    addonname = addon.getAddonInfo('name')
    line1 = 'Sorry! Could not find any video!'
    line2 = 'Please try to search anything else!'
    xbmcgui.Dialog().ok(addonname, line1, line2, file_host)  
    return

def viewmode():
    addon_settings = xbmcaddon.Addon(id='plugin.video.eroticshark')
    dview = int(addon_settings.getSetting('dview'))

    if dview == 0:
        xbmc.executebuiltin('Container.SetViewMode(50)')
    elif dview == 1:
        xbmc.executebuiltin('Container.SetViewMode(500)')

    return

def open_search_panel():
               
    search_text = ''
    keyb = xbmc.Keyboard('','Type your search text.')
    keyb.doModal()
 
    if (keyb.isConfirmed()):
        search_text = keyb.getText()

    return search_text

def main_directorys():
    url = build_url({'mode': 'porndoe', 'func': 'search_links', 'foldername': 'Search'})
    li = xbmcgui.ListItem('Search', iconImage=imageDir + 'search.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'porndoe', 'func': 'category_directorys', 'foldername': 'Categories'})
    li = xbmcgui.ListItem('Categories', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    video_links('/', '0')

    return

def category_directorys():
    top_url = 'http://porndoe.com/categories?sort=alpha'
            
    url_content = find_read_error(top_url)
    if url_content == 'HIBA':
        return

    category_links = re.compile('class="item"[^"]+"([^"]+).+title="([^"]+)').findall(url_content)

    if category_links:
        for cic in range(0, len(category_links)):
            url = build_url({'mode': 'porndoe', 'func': 'video_links', 'foldername': category_links[cic][0], 'pagenum': '0'})
            li = xbmcgui.ListItem(category_links[cic][1].decode('utf-8'), iconImage='DefaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)

    viewmode()
    xbmcplugin.endOfDirectory(addon_handle)

    return

def video_links(foldername, pagenum):
    pagenum = int(pagenum)
    pagenum += 1
    pagenum = str(pagenum)
    
    if re.compile('(/search)').findall(foldername):
        top_url = 'http://porndoe.com' + foldername + '&page=' + pagenum
        max_item = 24
    elif re.compile('(/category)').findall(foldername):
        top_url = 'http://porndoe.com' + foldername + '?page=' + pagenum
        max_item = 24
    else:
        top_url = 'http://porndoe.com' + foldername + '?page=' + pagenum
        max_item = 30

    url_content = find_read_error(top_url)
    if url_content == 'HIBA':
        return
    
    porn_links = re.compile('href="(/video[^"]+)"[^"]+"([^"]+)"[^d]+data-video-image="([^"]+)').findall(url_content)
    no_page = re.compile('(no-results)').findall(url_content)

    if len(porn_links) == max_item:
        next_page = True
    else:
        next_page = False

    if no_page:
        no_video('')
    else:
        for cic in range(0, len(porn_links)):
            url = build_url({'mode': 'porndoe', 'func': 'find_videourls', 'foldername': porn_links[cic][0], 'title': porn_links[cic][1], 'folderimage': porn_links[cic][2].replace(' ','%20')})
            download_args = 'DOWNLOAD, ' + porn_links[cic][0] + ',' + porn_links[cic][1].decode('utf-8')
            li = xbmcgui.ListItem(porn_links[cic][1].decode('utf-8'), iconImage=porn_links[cic][2].replace(' ','%20'))
            li.addContextMenuItems([ ('Download', 'XBMC.RunScript(' + download_script + ', ' + download_args + ')') ])
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)

        if pagenum != '1':
            url = build_url({'mode': 'back', 'func': 'video_links', 'foldername': foldername, 'pagenum': pagenum})
            li = xbmcgui.ListItem('[COLOR blue]<< Previous Page <<[/COLOR]', iconImage='DefaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=False)

        if next_page:
            url = build_url({'mode': 'porndoe', 'func': 'video_links', 'foldername': foldername, 'pagenum': pagenum})
            li = xbmcgui.ListItem('[COLOR green]>> Next Page >>[/COLOR]', iconImage='DefaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)

    viewmode()
    xbmcplugin.endOfDirectory(addon_handle)
 
    return

def search_links():

    search_text = open_search_panel()

    top_url = '/search?keywords=' + urllib.quote(search_text, '')

    video_links(top_url, '0')

    return

def find_videourls(foldername, foldertitle, folderimage, isdownload):
    top_url = 'http://porndoe.com' + foldername

    url_content = find_read_error(top_url)
    if url_content == 'HIBA':
        return

    direct_url = re.compile('file:[^"]+"([^"]+)".+label:"([^"]+)').findall(url_content)

    if direct_url:
        max_res = len(direct_url) - 1
        
        if isdownload == 'True':
            foldertitle = foldertitle[:41] + '.mp4'
            import download
            download.download_video(foldertitle, direct_url[max_res][0].replace('\\',''))
        else:
            videoitem = xbmcgui.ListItem(label=foldertitle, thumbnailImage=folderimage)
            videoitem.setInfo(type='Video', infoLabels={'Title': foldertitle})
            xbmc.Player().play(direct_url[max_res][0].replace('\\',''), videoitem)
    else:
        just_removed('Video')
    return

if sys.argv[1] == 'DOWNLOAD':
    foldername = sys.argv[2]
    foldertitle = sys.argv[3]
    find_videourls(foldername, foldertitle, 'None', 'True')
