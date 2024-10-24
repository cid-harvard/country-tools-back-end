from country_tools.country_tools_api.database.base import db_session


def sqlalchemy_filter(args, model, col):
    query = db_session.query(model)
    if col in args:
        query = query.filter(getattr(model, col) == args[col])
    return query
