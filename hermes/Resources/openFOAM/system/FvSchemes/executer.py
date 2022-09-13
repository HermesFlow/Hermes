from ..abstractSystemExecuter import abstractSystemExecuter

class FvSchemes(abstractSystemExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"FvSchemes")