#DEEZER SCRAPING

#=============================================================================
#IMPORTS & VARS
#=============================================================================

import urllib.request
from bs4 import BeautifulSoup
import json
import ast
import datetime

PUBIC_USER_ID = '1739153506'

URL_ALBUM = "https://www.deezer.com/br/profile/"+PUBIC_USER_ID+"/albums"
URL_SONG = "https://www.deezer.com/br/profile/"+PUBIC_USER_ID+"/loved"
URL_PLAYLIST = "https://www.deezer.com/br/profile/"+PUBIC_USER_ID+"/playlists"

OUTPUT_FILE_NAME_ALBUM = "DEEZER_ALBUM.txt"
OUTPUT_FILE_NAME_SONG = "DEEZER_SONG.txt"
OUTPUT_FILE_NAME_PLAYLIST = "DEEZER_PLAYLIST.txt"

URL,OUTPUT_FILE_NAME = URL_PLAYLIST,OUTPUT_FILE_NAME_PLAYLIST

SCRIPT_VAR = u"window.__DZR_APP_STATE__"

DEEZER_KEYS = { "ALBUM":{"ALB_TITLE":"ALB_TITLE","ART_NAME":"ART_NAME","ALB_ID":"ALB_ID"},
                "PLAYLIST":{"TITLE":"TITLE","URL":"PLAYLIST_ID"},
                "SONG":{"ALB_TITLE":"ALB_TITLE","SNG_TITLE":"SNG_TITLE","ART_NAME":"ART_NAME","ALB_ID":"ALB_ID"}}

"""
URL TEMPLATE :

    https://www.deezer.com/br/playlist/     [[[	    ID      ]]]
    https://www.deezer.com/br/album/        [[[	    ID      ]]]

"""

#=============================================================================
#FUNCTIONS
#=============================================================================

def GetHtml(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html = mybytes.decode("utf8")
    fp.close()
    return html

def SaveHtml(html, outputFileName):
    with open(outputFileName, mode="a+",encoding="utf-8") as text_file:
        text_file.writelines(html)

def ExtractScript(html_doc,script_var = SCRIPT_VAR):
    soup = BeautifulSoup(html_doc, 'html.parser')
    for script in soup.find_all('script'):
        if script_var in script.get_text():
            return script

def ExtractDict(bs4Type):
    print(bs4Type)
    return json.loads(bs4Type.get_text()[bs4Type.get_text().index("{"):])

def ExtractDeezer(deezerVarList,
                  type_ = "ALBUM",
                  keys = DEEZER_KEYS):
    #VARS
    deezer = []
    #LOOP
    for deezerVar in deezerVarList :
        dict_ = dict()
        for key in keys[type_]:
            dict_[key] = deezerVar[keys[type_][key]]
        deezer += [dict_]
    #RETURN
    return deezer

def GetPlaylistAlbums():
    return 0

def SaveData(dictData, type_= "ALBUM", keys = DEEZER_KEYS):
    #vars
    now = datetime.datetime.now()
    csvFile = open("./Output/{}_{}.txt".format(type_,now.strftime("%Y%m%d")), mode="w+",encoding="utf-8")
    #loop
    content = [";".join([key for key in keys[type_]])+"\n"]
    try :
        content += [ ";".join([dict_[key] for key in keys[type_]])+"\n" for dict_ in dictData]
    except :
        print("Error\t:\t{}".format(sys.exc_info()[0]))
    csvFile.writelines(content)
 
#=============================================================================
#PROG
#=============================================================================

if __name__=="__main__":

    albums = ExtractScript(GetHtml(URL_ALBUM))
    albums = ExtractDict(albums)

    playlists = ExtractScript(GetHtml(URL_PLAYLIST))
    playlists = ExtractDict(playlists)

    songs = ExtractScript(GetHtml(URL_SONG))
    songs = ExtractDict(songs)

    albums = ExtractDeezer(albums["TAB"]["albums"]["data"],"ALBUM")
    playlists = ExtractDeezer(playlists["TAB"]["playlists"]["data"],"PLAYLIST")
    songs = ExtractDeezer(songs["TAB"]["loved"]["data"],"SONG")

    print(len(albums),type(albums))
    print(len(playlists),type(albums))
    print(len(songs),type(albums))

    SaveData(albums,"ALBUM")
    SaveData(playlists,"PLAYLIST")
    SaveData(songs,"SONG")


