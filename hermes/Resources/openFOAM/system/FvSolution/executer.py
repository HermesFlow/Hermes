from ..abstractSystemExecuter import abstractSystemExecuter

class FvSolution(abstractSystemExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"FvSolution")