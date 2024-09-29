from project import request_channel_ids, request_video_ids, request_comments, request_likes_dislikes

from project import load_comments, load_stats # processes requested dataset from youtube api. Reutrns dictionary of comments and dictionary of stats.
                                  # mappings contain dictionary of channel names with list of video ids.
import os


#set all to true if dataset has not been created
REQUEST_CHANNEL_IDS = False 
REQUEST_VIDEO_IDS = False 
REQUEST_COMMENTS = False
REQUEST_STATS = False

SOURCE_DIR = f"./dataset"

def request_dataset():
    
    request_channel_ids(REQUEST_CHANNEL_IDS)
    request_video_ids(REQUEST_VIDEO_IDS) # set REQUEST variables to true if dataset has not been saved
    request_comments(REQUEST_COMMENTS)
    request_likes_dislikes(REQUEST_STATS)
                  


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