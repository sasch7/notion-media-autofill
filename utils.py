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

def parse_title_params(title):
    parts = title.split(';')
    main_title = parts[0].strip()
    year = None
    author = None

    for part in parts[1:]:
        if part.startswith('y'):
            year = part[1:]
        elif part.startswith('a'):
            author = part[1:]
    return main_title, year, author                        