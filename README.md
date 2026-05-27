Annotated lets add extra information in string validation
Before: 
q: str | None = None
After:
q: Annotated[str | None, Query(max_length=50)] = None