from ..abstractDispersionExecuter import abstractDispersionExecuter

class KinematicCloudProperties(abstractDispersionExecuter):
    def __init__(self,JSON):
        super().__init__(JSON,"KinematicCloudProperties")
