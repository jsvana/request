class MediaObject(object):
    def __init__(self, **kwargs):
        """Initializing from API objects"""
        # I'm lazy
        for key, value in kwargs.items():
            setattr(self, key, value)

class Movie(MediaObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = self.titles[0]
