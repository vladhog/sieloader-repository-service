from pydantic import BaseModel

class repo_info(BaseModel):
    name: str
    version: str
    email: str
    repositories: int

class addon_info(BaseModel):
    author: str
    description: str
    email: str
    version: str
    source: str
    size: int