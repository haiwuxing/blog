class Post(object):
    """代表一篇博文"""
    def __init__(self, id=None, title=None, text=None, created_at=None):
        self.id = id;
        self.title = title;
        self.text = text;
        self.created_at = created_at;