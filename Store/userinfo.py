UserInfo = {}
Session_id  = ''
def get_userinfo():
    return UserInfo

def set_userinfo(session_id, chatRoom, username):
    UserInfo[session_id] = {"chatRoom": chatRoom, "username": username}

