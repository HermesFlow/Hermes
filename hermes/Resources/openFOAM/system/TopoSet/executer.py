from ..abstractSystemExecuter import abstractSystemExecuter

class TopoSet(abstractSystemExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"TopoSet")