Annotated lets add extra information in string validation
Before: 
q: str | None = None
After:
q: Annotated[str | None, Query(max_length=50)] = None

Query Parameters
1. The Core Idea
Instead of writing out 4 or 5 separate query parameters inside your function arguments, you group them into a single, reusable Pydantic Model.

It turns a messy function layout into a clean one.

2. The Code Rules
Python
# 1. Create the reusable group
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0)
    offset: int = Field(0, ge=0)

# 2. Tell FastAPI to look in the URL
@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
The , Query() Rule: Pydantic models usually look inside a hidden request body. Adding , Query() forces FastAPI to look up at the URL query string instead.

The URL Match: A URL like ?limit=20&offset=5 automatically fills the variables inside filter_query.

3. The Strict Lock (Forbid Extras)
Normally, FastAPI ignores unknown query parameters. If you want to block typos or unauthorized inputs, add this single line inside your model class:

Python
class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # <-- Blocks unapproved inputs
    limit: int = 100
Result: If a user types ?limit=10&dog=bark, FastAPI instantly rejects the request with an error because dog is not on the approved list.
Response Model: Return type
async def create_item(item: Item) -> Item:
-> Item: is describing the return type of function