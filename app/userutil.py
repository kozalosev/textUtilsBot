def get_username_or_fullname(user: dict) -> str:
    if 'username' in user:
        username = "@" + user['username']
    else:
        username = user['first_name']
        if 'last_name' in user:
            username += " " + user['last_name']
    return username
