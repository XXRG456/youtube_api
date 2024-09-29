from .utils import API_KEY, save_pickle, load_pickle
from .utils import username_to_handle, usernames, get_channel_video_ids
import googleapiclient.discovery
import googleapiclient.errors
import os


def Channel_Id_Generator(channel_handle: str):
    
    api_service_name = "youtube"
    api_version = "v3"
    

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY
    )
    request = youtube.channels().list(
        part = "id",
        forHandle = channel_handle
    )
    response = request.execute()
    return {str(channel_handle): response['items'][0]['id']}

def Video_Id_Generator(channel_Id: str):
    api_service_name = "youtube"
    api_version = "v3"


    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY
    )
    request = youtube.search().list(
        part="id",
        channelId= channel_Id,
        maxResults=5,  # Maximum number of results per page (max allowed by YouTube Data API)
        type="video",
        order = "date"
    )
    response = request.execute()
    return response

def Comment_Generator(video_id, comment_typ):
    
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY
    )

    if comment_typ == 'top_comments':
        request = youtube.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            maxResults = 100, 
            order = 'relevance'
        )
        response = request.execute()
        return response
    
    if comment_typ == 'newest_comments':
        request = youtube.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            maxResults = 100, 
            order = 'time'
        )
        response = request.execute()
        return response


def Stats_Generator(video_id):
    
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY
    )
    
    request = youtube.videos().list(
        part = 'statistics',
        id = video_id,
    )

    response = request.execute()
    
    return response
    

    
SOURCE_DIR = f"./dataset"

#channel ids needed in order to request comments
def request_channel_ids(REQUEST_CHANNEL_IDS):
    if REQUEST_CHANNEL_IDS:
        if not os.path.exists(SOURCE_DIR): os.mkdir(SOURCE_DIR)
        
        for username, handle in username_to_handle.items():
            
            USERNAME_DIR = SOURCE_DIR + '/' + username
            if not os.path.exists(USERNAME_DIR): os.mkdir(USERNAME_DIR)
            
            CHANNEL_ID_DIR = USERNAME_DIR + '/' + 'channel_id'
            if not os.path.exists(CHANNEL_ID_DIR): os.mkdir(CHANNEL_ID_DIR)
            
            print(f"Grabbing {username} id")
            
            response = Channel_Id_Generator(handle)
            
            save_pickle(PATH=CHANNEL_ID_DIR + '/id.pickle', data=response)
        
#request video ids to request comments from
def request_video_ids(REQUEST_VIDEO_IDS):
    if REQUEST_VIDEO_IDS:
        
        for username, handle in username_to_handle.items():
            
            USERNAME_DIR = SOURCE_DIR + '/' + username
            VIDEO_ID_DIR = USERNAME_DIR + '/' + 'video_ids'
            
            if not os.path.exists(VIDEO_ID_DIR): os.mkdir(VIDEO_ID_DIR)
            
            channel_id = load_pickle(PATH=USERNAME_DIR + '/' + 'channel_id' + '/id.pickle')[handle]
            response = Video_Id_Generator(channel_id)
            
            print(f"saving responses to {VIDEO_ID_DIR}")
            save_pickle(PATH = VIDEO_ID_DIR + '/video_ids.pickle', data = response)
            
#request comments of type newest and top from request video ids            
def request_comments(REQUEST_COMMENTS):
    
    comment_typ = ['top_comments', 'newest_comments']
    if REQUEST_COMMENTS:
        
        for typ in comment_typ:
            for username in usernames:
                
                USERNAME_DIR = SOURCE_DIR + '/' + username
                VIDEO_ID_DIR = USERNAME_DIR + '/' + 'video_ids/video_ids.pickle'
                
                response = load_pickle(PATH=VIDEO_ID_DIR)
                video_ids = get_channel_video_ids(response)
                
                VIDEO_DIR = USERNAME_DIR + '/videos'
                if not os.path.exists(VIDEO_DIR): os.mkdir(VIDEO_DIR)
                
                for video_id in video_ids:
                    
                    COMMENTS_DIR = VIDEO_DIR + f'/{video_id}'
                    if not os.path.exists(COMMENTS_DIR): os.mkdir(COMMENTS_DIR)
                    
                    print(f"getting 100 {typ} comments from {username} from video: {video_id}")
                    response = Comment_Generator(video_id, typ)
                    save_pickle(PATH=COMMENTS_DIR + f'/{typ}.pickle', data=response)
    
def request_likes_dislikes(REQUEST_STATS):
    if REQUEST_STATS:
        for username in usernames:
            
            USERNAME_DIR = SOURCE_DIR + '/' + username
            VIDEO_ID_DIR = USERNAME_DIR + '/' + 'video_ids/video_ids.pickle'
            VIDEO_DIR = USERNAME_DIR + '/videos'
            
            if not os.path.exists(VIDEO_DIR): os.mkdir(VIDEO_DIR)
            
            video_ids = load_pickle(PATH=VIDEO_ID_DIR)
            video_ids = get_channel_video_ids(video_ids)
            
            for video_id in video_ids:
                
                STATS_DIR = VIDEO_DIR + f'/{video_id}'
                if not os.path.exists(STATS_DIR): os.mkdir(STATS_DIR)
                
                print(f"gettings stats for video {video_id} on channel: {username}")
                
                response = Stats_Generator(video_id)
                
                save_pickle(PATH=STATS_DIR + f"/statistics.pickle", data = response)
                
    
                