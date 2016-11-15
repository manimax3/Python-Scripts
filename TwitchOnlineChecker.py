import sqlite3
import json
import argparse
import webbrowser
from urllib.error import HTTPError
from urllib.request import urlopen
from pathlib import Path

CLIENT_ID = str("31g72q06t7txoegx19jeah27oyxf8rj")
REDIRECR_URI = str("https://manimax3.github.io")
DB_NAME = "storage.data"
TABLE_NAME = "streamers"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getDataFromStream(stream_name):
    url = "https://api.twitch.tv/kraken/streams/" + stream_name + "?response_type=&client_id=" + CLIENT_ID
    try:
        response = urlopen(url)
    except HTTPError:
        print("ERROR: TWITCH REST REQUEST")
        return {"stream" : None}
    return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))


def isonline(stream_data):
    return stream_data["stream"] is not None


def isonline_name(name):
    data = getDataFromStream(name)
    online = isonline(data)
    if online:
        return True, data['stream']['channel']['status'], data['stream']['channel']['url']
    else:
        return False, None, None


def database_setup():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE " + TABLE_NAME + " (name TEXT)")
    connection.commit()
    connection.close()


def db_existence_check():
    my_file = Path(DB_NAME)
    if not my_file.is_file():
        database_setup()


def database_stream_add(name):
    db_existence_check()
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO " + TABLE_NAME + " VALUES ('" + name + "')")
    connection.commit()
    connection.close()


def database_get_names():
    db_existence_check()
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM " + TABLE_NAME)
    names = cursor.fetchall()
    connection.commit()
    connection.close()
    return names


def database_remove(name):
    db_existence_check()
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM " + TABLE_NAME + " WHERE name='" + name + "'")
    connection.commit()
    connection.close()


def format_and_print_status_of(name, onlineonly, openinbrowser):
    status = isonline_name(name)
    if status[0]:
        print(name + " is currently:" + bcolors.OKGREEN +" ONLINE" + bcolors.ENDC + " Status: " + "'" + status[1] + "'")
        if openinbrowser:
            webbrowser.open(status[2], new=2)
    elif not onlineonly:
        print(name + " is currently: " + bcolors.FAIL +" OFFLINE" + bcolors.ENDC)



def check_names_in_db(onelineonly, openinbrowser):
    names = database_get_names()
    for name in names:
        format_and_print_status_of(name[0], onelineonly, openinbrowser)


def TwitchOnlineChecker(args):
    print("Test 1")
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--check', help="Checks all Streamers in the database or only the specified name",
                        action="store_true")
    parser.add_argument('-a', '--add', help="Adds a streamer to the database", action="store_true")
    parser.add_argument('-r', '--remove', help="Removes a Streamer from the database", action="store_true")
    parser.add_argument('-o', '--online', help="Only prints only streamers if specified together with -c",
                        action="store_true")
    parser.add_argument('-b', '--browser',
                        help="Tries to open all/one online stream(s) in the browser. Works only in combination with -c",
                        action="store_true")
    parser.add_argument('--name', help="username to add/remove", default='DEFAULT')
    args = parser.parse_args(args)

    if args.check and args.name == "DEFAULT":
        check_names_in_db(args.online, args.browser)
    elif args.check:
        format_and_print_status_of(args.name, False, args.browser)

    if args.add and args.name != 'DEFAULT':
        database_stream_add(args.name)
    elif args.add and args.name == 'DEFAULT':
        print("You should specifiy a name!")

    if args.remove and args.name != 'DEFAULT':
        database_remove(args.name)
    elif args.remove and args.name == 'DEFAULT':
        print("You should specifiy a name!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--check', help="Checks all Streamers in the database or only the specified name", action="store_true")
    parser.add_argument('-a', '--add', help="Adds a streamer to the database", action="store_true")
    parser.add_argument('-r', '--remove', help="Removes a Streamer from the database", action="store_true")
    parser.add_argument('-o', '--online', help="Only prints only streamers if specified together with -c", action="store_true")
    parser.add_argument('-b', '--browser', help="Tries to open all/one online stream(s) in the browser. Works only in combination with -c", action="store_true")
    parser.add_argument('--name', help="username to add/remove", default='DEFAULT')
    args = parser.parse_args()

    if args.check and args.name == "DEFAULT":
        check_names_in_db(args.online, args.browser)
    elif args.check:
        format_and_print_status_of(args.name, False, args.browser)

    if args.add and args.name != 'DEFAULT':
        database_stream_add(args.name)
    elif args.add and args.name == 'DEFAULT':
        print("You should specifiy a name!")

    if args.remove and args.name != 'DEFAULT':
        database_remove(args.name)
    elif args.remove and args.name == 'DEFAULT':
        print("You should specifiy a name!")




if __name__ == '__main__':
    main()