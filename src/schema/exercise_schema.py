from pydantic import BaseModel

class Exercise_Schema(BaseModel):
    muscle: int
    category: int
    name: str
    description: str
    videoUrl: str  
    imageUrl: str  
