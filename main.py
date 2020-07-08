import isodate
import googleapiclient.discovery
import googlemaps
import pandas as pd

'''
Table spec:
    video_id    Youtube video ID
    start?      start timestamp, int for seconds
    end?        end timestamp, int for seconds
    duration    total time, int for seconds
    continent   continent of video taken
    country     country of video taken
    city        city of video taken
    transport   one of car | train | run | walk
    night?      true if video taken at night
'''

temp_api_key_to_be_migrated_definitely = "AIzaSyCta9tiRjVtAq1RefBqpnZercOulGb1BTc"


def init():
    try:
        db_df = pd.read_csv("db.csv")
    except FileNotFoundError:
        db_df = pd.DataFrame(columns=[
            "video_id", "start", "end", "continent", "country", "city",
            "transport"
        ])
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=temp_api_key_to_be_migrated_definitely)
    gmaps = googlemaps.Client(key=temp_api_key_to_be_migrated_definitely)
    return db_df, youtube, gmaps


def add(database_df, youtube, gmaps):
    vid_id = input("Video ID: ")
    req = youtube.videos().list(
        part="snippet,contentDetails",
        id=vid_id
    )
    response = req.execute()
    print(response['items'][0]['snippet']['title'])
    duration = isodate.parse_duration(
        response['items'][0]['contentDetails']['duration']).total_seconds()
    print(gmaps.geocode(response['items'][0]['snippet']['title']))
    database_df.append({
        "video_id": vid_id,
        "start": 30,
        "end": "",
        "duration": duration,
        "continent": None,
        "country": None,
        "city": None,
        "transport": None
    }, ignore_index=True)
    return


def related(youtube):
    req = youtube.search().list(
        part="snippet",
        type="video",
        relatedToVideoId="wtLJPvx7-ys"
    )
    response = req.execute()


def edit():
    return


def remove():
    return


def main_loop(database_df, youtube, gmaps):
    actions_map = {
        "add": add,
        "edit": edit,
        "remove": remove,
    }
    while True:
        action = input("Select one of: add, edit, remove\n").lower()
        if action in actions_map:
            actions_map[action](database_df, youtube, gmaps)
            # SAVE
        else:
            continue


if __name__ == "__main__":
    print("Welcome to the commuter admin tool!")

    database_df, youtube, gmaps = init()

    main_loop(database_df, youtube, gmaps)
