from ..abstractSystemExecuter import abstractSystemExecuter

class SetFields(abstractSystemExecuter):
    def __init__(self,JSON):
        super().__init__(JSON,"SetFields")
