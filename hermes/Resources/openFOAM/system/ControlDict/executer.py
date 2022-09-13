from ..abstractSystemExecuter import abstractSystemExecuter

class ControlDict(abstractSystemExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"ControlDict")