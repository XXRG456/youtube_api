from project import request_channel_ids, request_video_ids, request_comments, request_likes_dislikes
from project import config
from project import load_comments, load_stats # processes requested dataset from youtube api. Reutrns dictionary of comments and dictionary of stats.
                                  # mappings contain dictionary of channel names with list of video ids.
import os




RETRIEVE_DATASET = config['retrieve_dataset'] # set to true if dataset has not been requested



SOURCE_DIR = f"./dataset"

def request_dataset():
    
    request_channel_ids(RETRIEVE_DATASET)
    request_video_ids(RETRIEVE_DATASET) 
    request_comments(RETRIEVE_DATASET)
    request_likes_dislikes(RETRIEVE_DATASET)
                  


if __name__ == '__main__':
    
    print("\nrunning...\n")
    
    request_dataset()
    
    """Uncomment after dataset has been requested"""
    # COMMENTS, mappings = load_comments(SOURCE_DIR)
    # STATS = load_stats(SOURCE_DIR)
    
    # for channel, data in STATS.items():
    #     print(f"Channel: {channel}")
    #     for video_id, stat in data.items():
    #         ratio = int(stat['likeCount']) / int(stat['viewCount']) * 100
    #         print(f"view-like ratio for video {video_id}: {ratio}")  
        
    #     print(f"\n")
    
    print("\nexecuted")