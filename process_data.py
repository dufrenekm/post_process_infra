#! /usr/bin/python3

from tkinter import filedialog, Tk
import rosbag
import cv2
from cv_bridge import CvBridge
import numpy as np
from time import sleep
import yaml
import math


def load_rosbag(file_path):
    bag = rosbag.Bag(file_path)
    cam = '/mounted_camera_0/compressed'
    topics = bag.get_type_and_topic_info()[1].keys()
    print(bag.get_type_and_topic_info()[1]['/mounted_camera_0/compressed'].message_count)
    print("we found the following topics: ")
    print(topics)
 
    print(bag.get_end_time()-bag.get_start_time())

    

    return bag, topics

def play_video(bag, topics):
    video_0_topic = '/mounted_camera_0/compressed'
    video_2_topic = '/mounted_camera_2/compressed'
    video_arm_rgb_topic = '/camera/color/image_raw/compressed'
    video_0_out = []
    video_2_out = []
    video_arm_rgb_out = []

    video_0_frames = 0
    video_2_frames = 0
    video_arm_rgb_frames = 0
    video_arm_d_frames = 0

    bag_time = bag.get_end_time()-bag.get_start_time()

    bridge = CvBridge()
    

    # Check if we have video 0 ("mounted_camera_0")
    if video_0_topic in topics:
        video_0 = bag.read_messages(video_0_topic)
        video_0_frames = bag.get_type_and_topic_info()[1][video_0_topic].message_count
        for i, b in enumerate(video_0):
            cv_image = bridge.compressed_imgmsg_to_cv2(b.message, desired_encoding='passthrough')
            video_0_out.append(cv_image)
            
    # Check if we have video 2 ("mounted_camera_2")
    if video_2_topic in topics:
        video_2 = bag.read_messages(video_2_topic)
        video_2_frames = bag.get_type_and_topic_info()[1][video_2_topic].message_count
        for i, b in enumerate(video_2):
            cv_image = bridge.compressed_imgmsg_to_cv2(b.message, desired_encoding='passthrough')
            video_2_out.append(cv_image)

    # Check if we have arm video
    if video_arm_rgb_topic in topics:
        video_arm_rgb = bag.read_messages(video_arm_rgb_topic)
        video_arm_rgb_frames = bag.get_type_and_topic_info()[1][video_arm_rgb_topic].message_count
        for i, b in enumerate(video_arm_rgb):
            cv_image = bridge.compressed_imgmsg_to_cv2(b.message, desired_encoding='passthrough')
            video_arm_rgb_out.append(cv_image)

            
    
    print("Len 0: ", len(video_0_out))
    print("Len 2: ", len(video_2_out))
    print("Len arm: ", len(video_arm_rgb_out))
    print("Arm video size: ", video_arm_rgb_out)
    cv2.namedWindow('image', flags=cv2.WINDOW_AUTOSIZE)

    number_frames = max(video_0_frames, video_2_frames)
    display_time = int(bag_time/number_frames*1000)
    for i in range(number_frames):
        out_image = np.hstack((video_0_out[int((i/number_frames)*video_0_frames)],video_2_out[int((i/number_frames)*video_2_frames)]))
        cv2.imshow('image',out_image)
        cv2.waitKey(display_time)


    



def select_files():
    print("Select the (files) you wish to view/process.")
    Tk().withdraw() # prevents an empty tkinter window from appearing
    file_list = filedialog.askopenfilenames() # Returns a tuple of selected files
    print("Number of files selected: ", len(file_list))
    return file_list

if __name__ == '__main__':
    test_num = int(input("""
    0) Display video
    1) Save video
    What do you want to do? (enter the number)
    """))

    file_list = select_files()

    if test_num == 0:
        bag, topics = load_rosbag(file_list[0])
        play_video(bag, topics)






















# alias python='/usr/bin/python3'
#alias python3='/usr/bin/python3'