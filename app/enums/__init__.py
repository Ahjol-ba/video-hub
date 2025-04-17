from enum import Enum

class SortField(Enum):
    DATE = 'date'
    PLAYBACK = 'playback'
    DURATION = 'duration'
    SIZE = 'size'


class ModelField(Enum):
    CATEGORY = 'category'
    TAG = 'tag'
    ERA = 'era'
    REGION = 'region'
    RESOLUTION = 'resolution'
    