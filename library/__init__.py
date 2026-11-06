"""Campus library API, organised in layers:

    routes/        HTTP only: read the request, call a service, build the response
    services/      use cases: the steps of "check out a book", "return a book", ...
    fines.py       pure business rules (fine rate, loan limits, amount owed)
    validation.py  checks on incoming data
    repositories/  all SQL, one module per table
    notifications  the only code that knows about outbox.txt
    serializers    database rows -> JSON-ready dicts
"""
