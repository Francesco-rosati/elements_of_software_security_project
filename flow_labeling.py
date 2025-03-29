# This file contains the code used to label the flows in the dataset


def get_flow_label(activity):
    """
    This function returns the label associated with the activity passed as parameter.
    :param activity: this is the activity coming from the type of captured flow.
    :return: the integer label associated with the activity.
    """

    # Dictionary containing the label for each activity
    label_dictionary = {
        'speaker-startup': 0,
        'camera-startup': 1,
        'play-music': 2,
        'volume-adjust': 3,
        'video-stream': 4,
        'call': 5
    }

    # Iterate over the dictionary and return the label if the activity is found
    for label, value in label_dictionary.items():
        if label in activity.lower():
            return value

    # Return -1 if no matching label is found
    return -1
