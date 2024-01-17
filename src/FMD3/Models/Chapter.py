import dataclasses


@dataclasses.dataclass
class Page():
    url:str
    filename:str

@dataclasses.dataclass
class Chapter():
    id:str
    volume:float|None
    number:float
    title:str
    pages:int
    scanlator:str|None
