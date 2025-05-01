import config

def get_media_type(database_id):
    if database_id == config.MOVIES_DATABASE_ID:
        return "movie"
    elif database_id == config.TVSERIES_DATABASE_ID:
        return "tvseries"
    elif database_id == config.BOOKS_DATABASE_ID:
        return "book"
    elif database_id == config.GAMES_DATABASE_ID:
        return "game"
    else:
        return "unknown"
