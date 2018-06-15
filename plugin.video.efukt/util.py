#-*- coding: utf-8 -*-

import sys, urllib, urllib2, re, cookielib, os
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, xbmcvfs

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.efukt'
addon = xbmcaddon.Addon(id=ADDON_ID)

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
       
def parseParameters(inputString=sys.argv[2]):
    """Parses a parameter string starting at the first ? found in inputString
    
    Argument:
    inputString: the string to be parsed, sys.argv[2] by default
    
    Returns a dictionary with parameter names as keys and parameter values as values
    """
    
    
    parameters = {}
    p1 = inputString.find('?')
    if p1 >= 0:
        splitParameters = inputString[p1 + 1:].split('&')
        for nameValuePair in splitParameters:
            try:
                if (len(nameValuePair) > 0):
                    pair = nameValuePair.split('=')
                    key = pair[0]
                    value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                    parameters[key] = value
                    #logError(value)
            except:
                pass
    return parameters

def extractAll(text, startText, endText):
    """
    Extract all occurences of a string within text that start with startText and end with endText
    
    Parameters:
    text: the text to be parsed
    startText: the starting tokem
    endText: the ending token
    
    Returns an array containing all occurences found, with tabs and newlines removed and leading whitespace removed
    """
    result = []
    start = 0
    pos = text.find(startText, start)
    while pos != -1:
        start = pos + startText.__len__()
        end = text.find(endText, start)
        result.append(text[start:end].replace('\n', '').replace('\t', '').lstrip())
        pos = text.find(startText, end)
    return result

def extract(text, startText, endText):
    """
    Extract the first occurence of a string within text that start with startText and end with endText
    
    Parameters:
    text: the text to be parsed
    startText: the starting tokem
    endText: the ending token
    
    Returns the string found between startText and endText, or None if the startText or endText is not found
    """
    start = text.find(startText, 0)
    if start != -1:
        start = start + startText.__len__()
        end = text.find(endText, start + 1)
        if end != -1:
            return text[start:end]
    return None      
    

def getURL(url, header=headers):
    try:
        req = urllib2.Request(url, headers=header)
            
        response = urllib2.urlopen(req)
        
        if response and response.getcode() == 200:
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO.StringIO( response.read())
                gzip_f = gzip.GzipFile(fileobj=buf)
                content = gzip_f.read()
            else:
                content = response.read()
            content = content.decode('utf-8', 'ignore')
            return content
        else:
            xbmc.log('Error Loading URL : '+str(response.getcode()), xbmc.LOGERROR)
    except urllib2.HTTPError as err:
        logError('Error Loading URL : '+url.encode("utf-8"))
        logError(str(err))
    except urllib2.URLError as err:
        logError('Error Loading URL : '+url.encode("utf-8"))
        logError(str(err))
    except socket.timeout as err:
        logError('Error Loading URL : '+url.encode("utf-8"))
        logError(str(err))
    
    return False
    
def addMenuItems(details, show=True):
    changed=False
    for detail in details:
        try:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title'].encode("utf-8"))+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].encode("utf-8"),"Plot": detail['plot']} )
        except:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title']).decode("utf-8")+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].decode("utf-8"),"Plot": detail['plot']} )
        
        
        if detail['isFolder']:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            liz.setProperty('IsPlayable', 'true')
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
            
    if show:
        xbmcplugin.endOfDirectory(int(sysarg))
def alert(alertText):
    dialog = xbmcgui.Dialog()
    ret = dialog.ok("EFUKT", alertText)
    
def select(list):
    dialog = xbmcgui.Dialog()
    ret = dialog.select("EFUKT", list)
    return ret
        
def notify(addonId, message, reportError=False, timeShown=5000):
    """Displays a notification to the user
    
    Parameters:
    addonId: the current addon id
    message: the message to be shown
    timeShown: the length of time for which the notification will be shown, in milliseconds, 5 seconds by default
    """
    addon = xbmcaddon.Addon(addonId)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))
    if reportError:
        logError(message)

def logError(error):
    try:
        xbmc.log("EFUKT Error - "+str(error.encode("utf-8")), xbmc.LOGERROR)
    except:
        xbmc.log("EFUKT Error - "+str(error), xbmc.LOGERROR)
    
def searchDialog(searchText="Please enter search text") :    
    keyb=xbmc.Keyboard('', searchText)
    keyb.doModal()
    searchText=''
    
    if (keyb.isConfirmed()) :
        searchText = keyb.getText()
    if searchText!='':
        return searchText
    return False

def progressStart(title, status):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create(title, status)
    xbmc.executebuiltin( "Dialog.Close(busydialog)" )
    progressUpdate(pDialog, 1, status)
    return pDialog

def progressStop(pDialog):
    pDialog.close
    
def progressCancelled(pDialog):
    if pDialog.iscanceled():
        pDialog.close
        return True
    return False

def progressUpdate(pDialog, progress, status):
    pDialog.update(int(progress), status)

def playMedia(title, thumbnail, link, mediaType='Video', library=True, title2="") :
    li = xbmcgui.ListItem(label=title2, iconImage=thumbnail, thumbnailImage=thumbnail, path=link)
    li.setInfo( "video", { "Title" : title } )
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    
    
# plugin specific code
def loadPage(params):
    page=""
    while "<video" not in page:
        page=getURL(params['url'])
    title=(page, '<h1 class="title">', '</h1>')
    poster=extract(page, 'poster="', '"')
    url=extract(page, '<source src="', '"')
    playMedia(title, poster, url.replace("&amp;", "&"))

def loadVideos(params):
    items=[]
    page=getURL(params['url'])
    videos=extractAll(page, '<div class="tile">', '</div>')
    for video in videos:
        parts=extractAll(video, '<a', '</a>')
        title=extract(parts[0], 'title="', '"')
        url=extract(parts[0], 'href="', '"')
        logError(url)
        poster=extract(parts[0], 'src="', '"')
        plot=extract(video, '<p class="desc oflow">', '<')
        items.append({
            "title": title,
            "url": url, 
            "mode":3, 
            "poster":poster,
            "icon":poster, 
            "fanart":poster,
            "type":"video", 
            "plot":"",
            "isFolder":False
        })
    if "fa fa-arrow-right" in page:
        nexts=extract(page, 'class="pagelinks', '</div>')
        nexts=extractAll(nexts, '<a ', '</a>')
        n=False
        for next in nexts:
            if n:
                items.append({
                    "title": "Next >",
                    "url": "http://efukt.com/"+extract(next, 'href="', '"'), 
                    "mode":2, 
                    "poster":"default.jpg",
                    "icon":"default.jpg", 
                    "fanart":"default.jpg",
                    "type":"video", 
                    "plot":"",
                    "isFolder":True
                })
                break
            elif "active" in next:
                n=True
    addMenuItems(items)