#!/usr/bin/python
# encoding=utf8
"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------

    Changelog:
        2018-05-13:
            Updated for when pages have malformed download links.

    Usage Examples:

    <dir>
        <title>Top Podcasts</title>
        <podbay>pbcategory/top</podbay>
    </dir>

    <dir>
        <title>Arts</title>
        <podbay>pbcategory/arts</podbay>
    </dir>

    <dir>
        <title>Business</title>
        <podbay>pbcategory/business</podbay>
    </dir>

    <dir>
        <title>Comedy</title>
        <podbay>pbcategory/comedy</podbay>
    </dir>

    <dir>
        <title>Education</title>
        <podbay>pbcategory/education</podbay>
    </dir>

    <dir>
        <title>Games and Hobbies</title>
        <podbay>pbcategory/games-and-hobbies</podbay>
    </dir>

    <dir>
        <title>Government and Organizations</title>
        <podbay>pbcategory/government-and-organizations</podbay>
    </dir>

    <dir>
        <title>Health</title>
        <podbay>pbcategory/health</podbay>
    </dir>

    <dir>
        <title>Kids and Family</title>
        <podbay>pbcategory/kids-and-family</podbay>
    </dir>

    <dir>
        <title>Music</title>
        <podbay>pbcategory/music</podbay>
    </dir>

    <dir>
        <title>News and Politics</title>
        <podbay>pbcategory/news-and-politics</podbay>
    </dir>

    <dir>
        <title>Religion and Spirituality</title>
        <podbay>pbcategory/religion-and-spirituality</podbay>
    </dir>

    <dir>
        <title>Science and Medicine</title>
        <podbay>pbcategory/science-and-medicine</podbay>
    </dir>

    <dir>
        <title>Society and Culture</title>
        <podbay>pbcategory/society-and-culture</podbay>
    </dir>

    <dir>
        <title>Sports and Recreation</title>
        <podbay>pbcategory/sports-and-recreation</podbay>
    </dir>

    <dir>
        <title>Technology</title>
        <podbay>pbcategory/technology</podbay>
    </dir>

    <dir>
        <title>TV and Film</title>
        <podbay>pbcategory/tv-and-film</podbay>
    </dir>

    <dir>
        <title>The Joe Rogan Experience</title>
        <podbay>pbshow/360084272</podbay>
    </dir>




"""

import json,re,requests,os,traceback,urlparse
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
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

pbshow_link = 'http://podbay.fm/show/'
pbcats_link = 'http://podbay.fm/browse/'

class WatchCartoon(Plugin):
    name = "podbay"

    def process_item(self, item_xml):
        if "<podbay>" in item_xml:
            item = JenItem(item_xml)
            if "pbcategory/" in item.get("podbay", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PBCats",
                    'url': item.get("podbay", ""),
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
            elif "pbshow/" in item.get("podbay", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PBShow",
                    'url': item.get("podbay", ""),
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
            elif "pbepisode/" in item.get("podbay", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PBEpisode",
                    'url': item.get("podbay", ""),
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
            result_item["properties"] = {
                'fanart_image': result_item["fanart"]
            }
            result_item['fanart_small'] = result_item["fanart"]
            return result_item


@route(mode='PBCats', args=["url"])
def get_pbcats(url):
    xml = ""
    url = url.replace('pbcategory/', '') # Strip our category tag off.
    try:
        url = urlparse.urljoin(pbcats_link, url)
        html = requests.get(url).content

        page_list = dom_parser.parseDOM(html, 'ul', attrs={'class': 'thumbnails'})[0]
        show_list = dom_parser.parseDOM(page_list, 'li', attrs={'class': 'span3'})
        for entry in show_list:
            try:
                show_url = dom_parser.parseDOM(entry, 'a', ret='href')[0]
                show_icon = dom_parser.parseDOM(entry, 'img', ret='src')[0]

                show_title = dom_parser.parseDOM(entry, 'h4')[0]
                show_title = refreshtitle(show_title)
                show_title = remove_non_ascii(show_title)

                xml += "<dir>"\
                       "    <title>%s</title>"\
                       "    <podbay>pbshow/%s</podbay>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "    <summary>%s</summary>"\
                       "</dir>" % (show_title,show_url,show_icon,show_title)
            except:
                continue
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='PBShow', args=["url"])
def get_pbshow(url):
    xml = ""
    url = url.replace('pbshow/', '') # Strip our show tag off.

    try:
        url = urlparse.urljoin(pbshow_link, url)
        html = requests.get(url).content

        show_icon = re.compile('<meta property="og:image" content="(.+?)"').findall(html)[0]
        table_content = dom_parser.parseDOM(html, 'div', attrs={'class': 'span8 well'})[0]
        table_rows = dom_parser.parseDOM(table_content, 'tr')
        for row in table_rows:
            if 'href' in row:
                ep_page, ep_summary, ep_title = re.compile('<a href="(.+?)".+?title="(.*?)">(.+?)</a>',re.DOTALL).findall(row)[0]
            else:
                continue
            xml += "<item>"\
                   "    <title>%s</title>"\
                   "    <podbay>pbepisode/%s</podbay>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <summary>%s</summary>"\
                   "</item>" % (ep_title,ep_page,show_icon,ep_summary)
    except:
        #failure = traceback.format_exc()
        #xbmcgui.Dialog().textviewer('Total Failure', str(failure))
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='PBEpisode', args=["url"])
def get_pbepisode(url):
    xml = ""
    url = url.replace('pbepisode/', '') # Strip our episode tag off.

    try:
        html = requests.get(url).content
        ep_icon = re.compile('property="og:image" content="(.*?)"',re.DOTALL).findall(html)[0]
        ep_title = re.compile('property="og:title" content="(.*?)"',re.DOTALL).findall(html)[0]
        ep_title = refreshtitle(ep_title)
        url = dom_parser.parseDOM(html, 'a', attrs={'class': 'btn btn-mini btn-primary'}, ret='href')[0]
        if not 'mp3' in url:
            url = re.compile('file: "(.*?)"',re.DOTALL).findall(html)[0]
        item = xbmcgui.ListItem(label=ep_title, path=url, iconImage=ep_icon, thumbnailImage=ep_icon)
        item.setInfo( type="Video", infoLabels={ "Title": ep_title } )
        import resolveurl
        koding.Play_Video(url,showbusy=False,ignore_dp=True,item=item,resolver=resolveurl)
    except:
        pass


def refreshtitle(title):
    title = replaceEscapeCodes(title)
    title = replaceHTMLCodes(title).replace('English Dubbed','[COLOR yellow](English Dubbed)[/COLOR]').replace('English Subbed','[COLOR orange](English Subbed)[/COLOR]')
    return title


def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    try:
        import html.parser as html_parser
    except:
        import HTMLParser as html_parser
    txt = html_parser.HTMLParser().unescape(txt)
    txt = html_parser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.strip()
    return txt


def replaceEscapeCodes(txt):
    try:
        import html.parser as html_parser
    except:
        import HTMLParser as html_parser
    txt = html_parser.HTMLParser().unescape(txt)
    return txt


def remove_non_ascii(text):
    try:
        text = text.decode('utf-8').replace(u'\xc2', u'A').replace(u'\xc3', u'A').replace(u'\xc4', u'A')
    except:
        pass
    return unidecode(text)

