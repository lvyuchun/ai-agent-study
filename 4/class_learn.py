from dataclasses import dataclass
@dataclass
class Learn:
    name: str
    score: int
    final_score: list[float]
@dataclass
class course:
    name: str
    score: int
    Learn_name: str
class learn_basic:
    def __init__(self,name,score,final_score):
        self.name = name
        self.score = score
        self.final_score = final_score
class Course:
    def __init__(self,name,score,learn_name):
        self.name = name
        self.score = score
        self.learn_name = learn_name
@dataclass
class Learn_game(Learn):
    thesis_title: str