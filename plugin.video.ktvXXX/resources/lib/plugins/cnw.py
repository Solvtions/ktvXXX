"""

    Copyright (C) 2018, MuadDib

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    -------------------------------------------------------------

"""

import requests,re,json,os,urlparse
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
next_icon = os.path.join(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')), 'resources', 'media', 'next.png')

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class CNW(Plugin):
    name = "cnw"

    def process_item(self, item_xml):
        if "<cnw>" in item_xml:
            item = JenItem(item_xml)
            if "http" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PlayCNW",
                    'url': item.get("cnw", ""),
                    'folder': False,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "category/" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_Cat",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "recent" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_Cat",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "popular" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_Cat",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "pornstar" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_ShowStarVids",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "search" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_Stars",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            result_item['fanart_small'] = result_item["fanart"]
            return result_item


@route(mode='CNW_Cat', args=["url"])
def category_cnw(url):
    xml = ""
    url = url.replace('category/', '')
    try:
        url = urlparse.urljoin('http://www.celebsnudeworld.com/', url)
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        
        cat_divs = dom_parser.parseDOM(html, 'ul', attrs={'class':'videos'})[0]
        vid_entries = dom_parser.parseDOM(cat_divs, 'li')
        for vid_section in vid_entries:
            thumbnail = urlparse.urljoin('http://www.celebsnudeworld.com/', re.compile('src="(.+?)"',re.DOTALL).findall(str(vid_section))[0])
            vid_page_url, title = re.compile('href="(.+?)"\stitle="(.+?)"',re.DOTALL).findall(str(vid_section))[0]
            vid_page_url = urlparse.urljoin('http://www.celebsnudeworld.com/', vid_page_url)
            xml += "<item>"\
                   "    <title>%s</title>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <cnw>%s</cnw>"\
                   "    <summary>%s</summary>"\
                   "</item>" % (title,thumbnail,vid_page_url, title)

        try:
            try:
                next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'prevnext'}, ret='href')[1]
            except:
                next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'prevnext'}, ret='href')[0]
            next_page = next_page.replace('/', '', 1)
            xml += "<dir>"\
                   "    <title>Next Page</title>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <cnw>category/%s</cnw>"\
                   "</dir>" % (next_icon,next_page)
        except:
            pass
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='CNW_ShowStarVids', args=["url"])
def pornstar_vids_cnw(url):
    xml = ""
    url = url.replace('category/', '')
    try:
        xml += "<dir>"\
               "    <title>Celebs Nude World Home</title>"\
               "    <link>file://cnw/main.xml</link>"\
               "</dir>"

        url = urlparse.urljoin('http://www.celebsnudeworld.com/', url)
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        
        cat_divs = dom_parser.parseDOM(html, 'ul', attrs={'class':'videos'})[0]
        vid_entries = dom_parser.parseDOM(cat_divs, 'li')
        for vid_section in vid_entries:
            thumbnail = urlparse.urljoin('http://www.celebsnudeworld.com/', re.compile('src="(.+?)"',re.DOTALL).findall(str(vid_section))[0])
            vid_page_url, title = re.compile('href="(.+?)"\stitle="(.+?)"',re.DOTALL).findall(str(vid_section))[0]
            vid_page_url = urlparse.urljoin('http://www.celebsnudeworld.com/', vid_page_url)
            xml += "<item>"\
                   "    <title>%s</title>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <cnw>%s</cnw>"\
                   "    <summary>%s</summary>"\
                   "</item>" % (title,thumbnail,vid_page_url, title)

        try:
            try:
                next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'prevnext'}, ret='href')[1]
            except:
                next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'prevnext'}, ret='href')[0]
            next_page = next_page.replace('/', '', 1)
            xml += "<dir>"\
                   "    <title>Next Page</title>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <cnw>category/%s</cnw>"\
                   "</dir>" % (next_icon,next_page)
        except:
            pass
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='CNW_Stars', args=["url"])
def pornstars_cnw(url):
    xml = ""
    try:
        keyboard = xbmc.Keyboard('', 'Search for')
        keyboard.doModal()
        if keyboard.isConfirmed() != None and keyboard.isConfirmed() != "":
            search = keyboard.getText()
        else:
            return

        if search == None or search == "":
            xml += "<item>"\
                   "    <title>Search Cancelled</title>"\
                   "    <heading></heading>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "</item>" % (addon_icon)
            jenlist = JenList(xml)
            display_list(jenlist.get_list(), jenlist.get_content_type())
            return

        total = 0

        try:
            search_url = 'http://www.celebsnudeworld.com/search/pornstar/?s=%s' % search.replace(' ', '+')
            html = requests.get(search_url).content
            results = dom_parser.parseDOM(html, 'div', attrs={'class':'model'})

            if len(results) == 0:
                dialog = xbmcgui.Dialog()
                dialog.ok('Search Results', 'Search Results are empty')
                return
            for star in results:
                thumbnail = urlparse.urljoin('http://www.celebsnudeworld.com/', re.compile('src="(.+?)"',re.DOTALL).findall(str(star))[0])
                vid_page_url, title = re.compile('href="(.+?)"\stitle="(.+?)"',re.DOTALL).findall(str(star))[0]

                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "    <cnw>%s</cnw>"\
                       "    <summary>%s</summary>"\
                       "</item>" % (title,thumbnail,vid_page_url, title)
                total += 1
        except:
            pass
    except:
        pass

    if total > 0:
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='PlayCNW', args=["url"])
def play_cnw(url):
    try:
        headers = {'User_Agent':User_Agent}
        vid_html = requests.get(url,headers=headers).content
        qualities = re.compile('label="(.+?)"',re.DOTALL).findall(str(vid_html))

        selected = xbmcgui.Dialog().select('Select Quality',qualities)
        if selected ==  -1:
            return        

        vid_url = re.compile('source src="(.+?)"\stype=".+?"\slabel="%s"' % (qualities[selected]),re.DOTALL).findall(str(vid_html))[0]
        xbmc.executebuiltin("PlayMedia(%s)" % vid_url)
    except:
        return

def remove_non_ascii(text):
    return unidecode(text)

