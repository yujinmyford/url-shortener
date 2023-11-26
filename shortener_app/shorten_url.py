from fastapi import FastAPI, Path, Query, HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from typing import Optional
from pydantic import BaseModel
import pyshorteners


app = FastAPI()
type_tiny = pyshorteners.Shortener()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {}

urls = {}

# # Path parameter, item_id
# # the gt and lt checks for greater than, less than
# @app.get("/get-item/{item_id}")
# def get_item(item_id: int = Path(None, description="The ID of the item you'd like to view."), gt=0):
#     return inventory[item_id]


# # Query parameter, test is required, name is not
# @app.get("/get-by-name")
# def get_item(name: Optional[str] = None):
#     for item_id in inventory:
#         if inventory[item_id].name == name:
#             return inventory[item_id]
#     raise HTTPException(status_code=404, detail="Item name not found.")

# @app.post("/create_item/{item_id}")
# def create_item(item_id: int, item: Item):
#     if item_id in inventory:
#         raise HTTPException(status_code=40, detail="Item ID already exists.")
    
#     # inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
#     # Smarter way
#     inventory[item_id] = item
#     return inventory[item_id]

# @app.put("/update-item/{item_id}")
# def update_item(item_id: int, item: UpdateItem):
#     if item_id not in inventory:
#         raise HTTPException(status_code=404, detail="Item ID does not exist.")
    
#     # Update item we already have
#     if item.name != None:
#         inventory[item_id].name = item.name
#     if item.price != None:
#         inventory[item_id].price = item.price
#     if item.brand != None:
#         inventory[item_id].brand = item.brand
    
    
#     return inventory[item_id]

# @app.delete("/delete-item")
# def delete_item(item_id: int = Query(..., description="The ID of the item to delete"), gt=0):
#     if item_id not in inventory:
#         raise HTTPException(status_code=404, detail="Item ID does not exist.")
#     del inventory[item_id]
#     return {"Success": "Item deleted"}


# @app.post("/create_item/{item_id}")
# def create_item(item_id: int, item: Item):
#     if item_id in inventory:
#         raise HTTPException(status_code=40, detail="Item ID already exists.")
    
#     # inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
#     # Smarter way
#     inventory[item_id] = item
#     return inventory[item_id]



# @app.post("/create_item/{item_id}")
# def create_item(item_id: int, item: Item):
#     if item_id in inventory:
#         raise HTTPException(status_code=40, detail="Item ID already exists.")
    
#     # inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
#     # Smarter way
#     inventory[item_id] = item
#     return inventory[item_id]

@app.post("/shorten_url")
def shorten_url(original_url: str, short_url: Optional[str] = None):
    for url in urls:
        if urls[url] == short_url:
            raise HTTPException(status_code=404, detail="Short URL '" + short_url + "' already exists")
    if short_url:
        urls[original_url] = short_url
        return short_url
    else:
        new_short_url = type_tiny.tinyurl.short(original_url)
        urls[original_url] = new_short_url
        return new_short_url


# @app.get("/get-item/{item_id}")
# def get_item(item_id: int = Path(None, description="The ID of the item you'd like to view."), gt=0):
#     return inventory[item_id]


@app.get("/list_urls")
def list_urls():
    return urls

@app.get("/redirect", response_class=RedirectResponse)
async def redirect(short_url: str):
    for url in urls:
        if urls[url] == short_url:
            return url
    raise HTTPException(status_code=404, detail="No URL found for '" + short_url + "' found.")