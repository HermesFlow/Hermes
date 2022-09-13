from ..abstractSystemExecuter import abstractSystemExecuter

class CreatePatch(abstractSystemExecuter):
    def __init__(self,JSON):
        super().__init__(JSON,"CreatePatch")
