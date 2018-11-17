from googleapiclient.discovery import build
from operator import itemgetter
import pandas as pd

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = "developer_key"


def get_video_statistics(youtube_video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    results = youtube.videos().list(
        part = "statistics",
        id = youtube_video_id,
    ).execute()
    yt_statistics = results.get('items')[0]["statistics"]

    if 'likeCount' in yt_statistics :
        likes = int(yt_statistics["likeCount"])
    else :
        likes = 0

    if 'dislikeCount' in yt_statistics :
        dislikes = int(yt_statistics["dislikeCount"])
    else :
        dislikes = 0

    if 'viewCount' in yt_statistics :
        view_count = int(yt_statistics["viewCount"])
    else :
        view_count = 0

    return likes, dislikes, view_count



# url_list means youtube video ID list !
# input = list, return = dataframe->Series
def youtube_rating_sort(url_list) :
    
    sorted_list = []
    for s in url_list :
        temp_like, temp_dislike, temp_view = get_video_statistics(s)
        try : 
            temp = [{"popularity":(temp_like / float(temp_dislike)), "view_count": temp_view, "video_id": s}]
        except :
            temp = [{"popularity":(temp_like), "view_count": temp_view, "video_id": s}]
            sorted_list += temp
        sorted_list += temp

    sorted_list = sorted(sorted_list, key=itemgetter('popularity', 'view_count'), reverse=True)
    sorted_list = pd.DataFrame(sorted_list)

    return sorted_list['video_id'].tolist()