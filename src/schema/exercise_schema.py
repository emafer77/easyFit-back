from pydantic import BaseModel

class Exercise_Schema(BaseModel):
    name: str
    description: str
    muscle: int
    category: int
    videoUrl: str  
    imageUrl: str  
