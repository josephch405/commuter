import isodate
import googleapiclient.discovery
import googlemaps
import pandas as pd
import os

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

temp_api_key_to_be_migrated_definitely = os.getenv("COMMUTER_API_KEY")


COLUMNS = [
    "video_id", "title", "description", "start", "end", "continent", "country", "city",
    "transport", "title_geocode", "description_geocode"
]

CSV_PATH = "db.csv"


def init():
    try:
        db_df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        db_df = pd.DataFrame(columns=COLUMNS)
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=temp_api_key_to_be_migrated_definitely)
    gmaps = googlemaps.Client(key=temp_api_key_to_be_migrated_definitely)
    return db_df, youtube, gmaps


def add(database_df: pd.DataFrame, youtube, gmaps: googlemaps.Client) -> pd.DataFrame:
    video_id = input("Video ID: ")
    req = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    )
    if (database_df['video_id'] == video_id).any():
        print("Video already exists!")
        return
    response = req.execute()
    print(response['items'][0]['snippet']['title'])
    print(response['items'][0]['snippet'].keys())
    duration = isodate.parse_duration(
        response['items'][0]['contentDetails']['duration']).total_seconds()
    title = response['items'][0]['snippet']['title']
    description = response['items'][0]['snippet']['description']
    channel_id = response['items'][0]['snippet']['channelId']
    database_df = database_df.append({
        "video_id": video_id,
        "title": title,
        "description": description,
        "channel_id": channel_id,
        "start": 30,
        "end": "",
        "duration": duration,
        "continent": None,
        "country": None,
        "city": None,
        "transport": None,
        "title_geocode": gmaps.geocode(title),
        "description_geocode": gmaps.geocode(description),
    }, ignore_index=True)
    return database_df


def related(youtube):
    req = youtube.search().list(
        part="snippet",
        type="video",
        relatedToVideoId="wtLJPvx7-ys"
    )
    response = req.execute()


def edit(database_df: pd.DataFrame):
    return database_df


def remove(database_df: pd.DataFrame):
    return database_df


def main_loop(database_df: pd.DataFrame, youtube, gmaps):
    actions_map = {
        "add": add,
        "edit": edit,
        "remove": remove,
    }
    while True:
        action = input("Select one of: add, edit, remove\n").lower()
        if action in actions_map:
            database_df = actions_map[action](database_df, youtube, gmaps)
            database_df.to_csv(CSV_PATH, index=False)
        else:
            continue


if __name__ == "__main__":
    print("Welcome to the commuter admin tool!")

    database_df, youtube, gmaps = init()

    main_loop(database_df, youtube, gmaps)
