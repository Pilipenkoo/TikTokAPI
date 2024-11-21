# entities/follower.py

class Follower:
    def __init__(self, username: str, profile_url: str):
        self.username = username
        self.profile_url = profile_url

    def __eq__(self, other):
        if isinstance(other, Follower):
            return self.username == other.username
        return False

    def __hash__(self):
        return hash(self.username)
