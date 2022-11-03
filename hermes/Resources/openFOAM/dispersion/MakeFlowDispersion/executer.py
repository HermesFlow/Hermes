from ....executers.abstractExecuter import abstractExecuter
import logging
import os

class MakeFlowDispersion(abstractExecuter):


    def run(self, **inputs):
        logger = logging.getLogger('luigi-interface')
        logger.info("Creating flow for dispersion")
        try:
            from hera import toolkitHome
        except ImportError:
            logger.error("This node can be used only if hera is installed!!.")
            raise ValueError("This node can be used only if hera is installed!!.")

        tk = toolkitHome.getToolkit(toolkitName=toolkitHome.SIMULATIONS_OPENFOAM, projectName="tmp")
        logtk = toolkitHome.getToolkit(toolkitName=toolkitHome.LOGGING, projectName=None)

        logtk.addLogger(loggerName="simulations.openFoam", handlers=['console'], level='DEBUG', propagate=False)

        overwriteFlag = inputs.get("overwriteFlowIfExists",False)
        basename = f"{inputs['name']}_Flow"
        flowdata = inputs

        case = tk.prepareFlowFieldForDispersion(flowData=flowdata, simulationGroup=basename, useDBSupport=False)
        if inputs.get("buildDistanceFromWalls",False):
            logger.info(f"Preparing the Cell heights with:")
            logger.info(f" foamJob -parallel -wait indoorDistanceFromWalls  -case {case} -time 0:")
            logger.info("If Openfoam is not Loaded, run it explitely. ")
            ret = os.system(f"cd {case};foamJob -parallel -wait indoorDistanceFromWalls  -case {case} -time 0: ;cd ..")
            if ret != 0:
                raise ValueError("Openfoam not installed, or indoorDistanceFromWalls does not exist!. ")
        else:
            logger.info(f"buildDistanceFromWalls flag is False (or does not exist)")




        return dict(MakeFlowDispersion="MakeFlowDispersion",flowField=case)