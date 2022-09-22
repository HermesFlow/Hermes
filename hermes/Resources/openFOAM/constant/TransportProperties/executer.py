from ..abstractConstantExecuter import abstractConstantExecuter

class TransportProperties(abstractConstantExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"TransportProperties")
