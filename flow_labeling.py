# This file contains the code used to label the flows in the dataset


def get_flow_label(activity):
    """
    This function returns the label associated with the activity passed as parameter.
    :param activity: this is the activity coming from the type of captured flow.
    :return: the integer label associated with the activity.
    """

    # Dictionary containing the label for each activity
    label_dictionary = {
        'stream_onoff': 0,
        'fan_onoff': 1,
        'robot_mode': 2,
        'intensity': 3,
        'quickrun': 4,
        'color': 5,
        'armdisarm': 6,
        'photo': 7,
        'watch': 8,
        'hvac': 9,
        'lockunlock': 10,
        'onoff': 11,
        'mode': 12,
        'fan': 13,
        'startup': 14,
        'video_stream': 15,
        'night_vision': 16,
        'weather': 17,
        'wake_word': 18,
        'volume_adjust': 19,
        'play_video': 20
    }

    # Iterate over the dictionary and return the label if the activity is found
    for label, value in label_dictionary.items():
        if label in activity.lower():
            return value

    # Return -1 if no matching label is found
    return -1
