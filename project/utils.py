import pickle
import os
import re
from dotenv import load_dotenv # type: ignore


load_dotenv()
API_KEY = os.getenv('DEVELOPER_KEY')

channel_handles = ['@Sidemen', '@BetaSquad', '@JoeFazer', '@Jynxzi']
sort_typ = ['top', 'newest']


def get_username():
    return [channel.split("@")[1] for channel in channel_handles]

usernames = get_username()

def load_pickle(PATH):
    with open(PATH, "rb") as f:
        data = pickle.load(f)
    return data

def save_pickle(PATH, data):
    assert '.pickle' in PATH.split("/")[-1], "must be a pickle file"
    with open(PATH, "wb") as f:
        pickle.dump(data, f)        

username_to_handle = dict(zip(get_username(), channel_handles))

def get_channel_video_ids(data):
    
    return [i['id']['videoId'] for i in data['items']]

def find_files(DIR):
    
    paths = []
    for root, dirs, files in os.walk(DIR):
        for file in files:
            paths.append(os.path.join(root, file))
    return paths

def find_dirs(DIR):
    
    paths = []
    for root, dirs, files in os.walk(DIR):
        for name in dirs:
            paths.append(os.path.join(root, name))
    return paths

def load_comments(DIR):
    SOURCE_DIR = DIR
    COMMENTS = {}
    for channel in usernames:
        CHANNELS = {}
        VIDEO_DIR = SOURCE_DIR + '/' + channel + '/videos'
        paths = find_dirs(VIDEO_DIR)
        for path in paths:
            
            dirs = find_files(path)
            DATA = {}
            for dir in dirs:
                
                sort = re.findall(r'(?<=\\)[\w0-9_]*(?=\.pickle)', dir)[0]
                if sort not in ['newest_comments', 'top_comments']: continue
                
                video = re.findall(r'(?<=\\)[\w0-9_-]*(?=\\)', dir)[0]
                
                response = load_pickle(dir)
                
                DATA[sort] = [user['snippet']['topLevelComment']['snippet']['textOriginal'] for user in response['items']]
            CHANNELS[video] = DATA
        COMMENTS[channel] = CHANNELS

    mappings = {}
    for key_1, _ in COMMENTS.items():
        vid_ids = []
        for key_2, _ in COMMENTS[key_1].items():
            vid_ids.append(key_2)
        mappings[key_1] = vid_ids
        
    return COMMENTS, mappings

def load_stats(DIR):
    SOURCE_DIR = DIR
    STATS = {}
    for channel in usernames:
        STATS[channel] = {}
        VIDEO_DIR = SOURCE_DIR + f'/{channel}/videos'
        paths = find_dirs(VIDEO_DIR)
        for path in paths:
            dirs = find_files(path)

            for dir in dirs:
                
                sort = re.findall(r'(?<=\\)[\w0-9_]*(?=\.pickle)', dir)[0]
                if sort in ['newest_comments', 'top_comments']: continue
                
                video = re.findall(r'(?<=\\)[\w0-9_-]*(?=\\)', dir)[0]
                response = load_pickle(dir)
                STATS[channel][video] = response['items'][0]['statistics']
    return STATS
            
            
        
