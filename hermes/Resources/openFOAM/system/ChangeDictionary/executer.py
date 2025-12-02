from ..abstractSystemExecuter import abstractSystemExecuter

class ChangeDictionary(abstractSystemExecuter):

    def __init__(self,JSON, full_workflow=None):
        super().__init__(JSON,"ChangeDictionary", full_workflow=full_workflow)

