def sqlalchemy_filter(args, model, col):
    query = db_session.query(model)
    if col in args:
        query = query.filter(getattr(model, col) == args[col])
    return query
