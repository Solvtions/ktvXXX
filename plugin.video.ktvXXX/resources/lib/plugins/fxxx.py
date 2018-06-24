"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------


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

class FXXXMovies(Plugin):
    name = "fxxxmovies"

    def process_item(self, item_xml):
        if "<fxxxmovies>" in item_xml:
            item = JenItem(item_xml)
            if "http" in item.get("fxxxmovies", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PlayFXXX",
                    'url': item.get("fxxxmovies", ""),
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
            elif "fxmtag/" in item.get("fxxxmovies", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "FXXXTags",
                    'url': item.get("fxxxmovies", ""),
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


@route(mode='FXXXTags', args=["url"])
def fxxx_tags(url):
    xml = ""
    url = url.replace('fxmtag/', '')
    orig_tag = url.split("/")[0]
    try:
        url = urlparse.urljoin('http://fullxxxmovies.net/tag/', url)
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        try:
            tag_divs = dom_parser.parseDOM(html, 'div', attrs={'id':'mainAnninapro'})[0]
            vid_entries = dom_parser.parseDOM(tag_divs, 'article')
            for vid_section in vid_entries:
                thumbnail = re.compile('src="(.+?)"',re.DOTALL).findall(str(vid_section))[0]
                vid_page_url, title = re.compile('h3 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h3',re.DOTALL).findall(str(vid_section))[0]
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <meta>"\
                       "        <summary>%s</summary>"\
                       "    </meta>"\
                       "    <fxxxmovies>%s</fxxxmovies>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,title,vid_page_url,thumbnail)
        except:
            pass

        try:
            try:
                next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'next page-numbers'}, ret='href')[0]
                next_page = next_page.split("/")[-2]
                xml += "<dir>"\
                       "    <title>Next Page</title>"\
                       "    <meta>"\
                       "        <summary>Click here for more porn bitches!</summary>"\
                       "    </meta>"\
                       "    <fxxxmovies>fxmtag/%s/page/%s</fxxxmovies>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</dir>" % (orig_tag,next_page,next_icon)
            except:
                pass
        except:
            pass
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

ignore_items = {'imgcloud','depfile','rapidgator','vidlox'}

@route(mode='PlayFXXX', args=["url"])
def fxxx_play(url):
    try:
        progress_dialog = xbmcgui.DialogProgress()
        progress_dialog.create("Finding Streams", "Get your tissues ready while we find the movie....")
        progress = 0
        headers = {'User_Agent':User_Agent}
        vid_html = requests.get(url,headers=headers).content
        the_item = dom_parser.parseDOM(vid_html, 'div', attrs={'class':'entry-content'})[0]
        progress += 10
        progress_dialog.update(progress)
        streams = re.compile('href="(.+?)"',re.DOTALL).findall(str(the_item))
        try:
            title = re.compile('<em>(.+?)</em>',re.DOTALL).findall(str(the_item))[0]
        except:
            title = re.compile('property="og:title" content="(.+?)"',re.DOTALL).findall(str(vid_html))[0]
        progress += 10
        progress_dialog.update(progress)
        names = []
        sources = []
        for stream in streams:
            progress += 5
            progress_dialog.update(progress)
            if 'securely.link' in stream:
                response = requests.get(stream)
                stream = response.url
            elif any(x in stream for x in ignore_items):
                continue
            if 'openload' in stream:
                names.append('Openload')
                sources.append(stream)
            elif 'streamango' in stream:
                names.append('Streamango')
                sources.append(stream)

        progress_dialog.close()
        selected = xbmcgui.Dialog().select('Select Source',names)
        if selected ==  -1:
            return        

        item = xbmcgui.ListItem(label=title, path=sources[selected], iconImage=addon_icon, thumbnailImage=addon_icon)
        item.setInfo( type="Video", infoLabels={ "Title": title } )
        import resolveurl
        koding.Play_Video(sources[selected],showbusy=False,ignore_dp=True,item=item,resolver=resolveurl)
    except:
        return


def remove_non_ascii(text):
    return unidecode(text)

