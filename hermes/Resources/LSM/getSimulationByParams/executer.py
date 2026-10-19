from ...executers.abstractExecuter import abstractExecuter


class getSimulationByParams(abstractExecuter):
    """
        Runs a Fortran LSM simulation.

        inputs:
            ProjectName : str, The class path string to the class
            Template : str, The class path string to the class
            SimulationParameters : str, The class path string to the class
            SimulationName : str, The class path string to the class
    """

    def _defaultParameters(self):
        return dict(
            output=[],

            inputs=["ProjectName","Template", "SimulationParameters", "SimulationName"],
            webGUI={},
            parameters={}
        )

    @staticmethod
    def testParamValues(params: dict[str, any]):
        possible_simulation_params = ['TopoFile', 'flat', 'TopoXmin', 'TopoXmax', 'TopoYmin', 'TopoYmax', 'TopoXn', 'TopoYn', 'sourceRatioX', 'sourceRatioY', 'releaseDuration', 'releaseHeight', 'windSpeed', 'windDir', 'inversionHeight', 'savedt', 'duration', 'nParticles', 'savedx', 'savedy', 'savedz', 'StationsFile', 'homogeneousWind', 'particles3D', 'wind3D', 'n_vdep', 'lineSource', 'stability']

        for param in ["ProjectName", "SimulationName"]:
            passed, status_message = abstractExecuter.checkParamType(params, param, str, required=True)
            if not passed:
                return passed, status_message
        
        passed, status_message = abstractExecuter.checkParamType(params, "Template", str, required=False)
        if not passed:
            return passed, status_message
        
        if abstractExecuter.isParamTestable(params, "ProjectName"):
            import hera
            from hera.datalayer.project import getProjectList
            passed, status_message = abstractExecuter.checkParamAgainstList(params, "ProjectName", getProjectList(), False)
            if not passed:
                return passed, status_message
            lsm_tk = hera.toolkitHome.getToolkit(hera.toolkitHome.LSM, projectName=params["ProjectName"])
            abstractExecuter.checkParamAgainstList(params, "Template", list(lsm_tk.getTemplatesTable().template), False)
            if not passed:
                return passed, status_message
        

        if abstractExecuter.isParamTestable(params, "SimulationParameters"):
            passed, status_message = abstractExecuter.checkParamType(params, "SimulationParameters", dict, required=False)
            if not passed:
                return passed, status_message
            for simParam in params['SimulationParameters']:
                passed, status_message = abstractExecuter.checkParamAgainstList(simParam, simParam, possible_simulation_params, required=False)
                if not passed:
                    return passed, status_message
        
        return True, ""

    
    def run(self, **inputs):
        self.logger.info("Starting LSM simulation")

        from hera import toolkitHome
        from hera.datalayer import Project
        from hera.utils.jsonutils import JSONToConfiguration


        if 'ProjectName' not in inputs:
            raise Exception("Node wasn't given project name through `ProjectName` parameter")
        p = Project(projectName=inputs['ProjectName'])


        if 'SimulationName' not in inputs:
            raise Exception("Node wasn't given simulation name through `SimulationName` parameter")
        simulation_name = inputs['SimulationName']
        
        template = inputs.get("Template", "v4-general")

        old_lsm_toolkit = toolkitHome.getToolkit(toolkitName=toolkitHome.LSM, projectName=p.projectName, to_xarray=True, to_database=False, forceKeep=True)

        lsm_templates = old_lsm_toolkit.getTemplates(template=template)
        if len(lsm_templates) == 0:
            raise Exception("Template v4-general isn't loaded to the project. Please load the relevant repository for v4-general into the project.")
        lsm_template = lsm_templates[0]

        sim_params = inputs.get('SimulationParameters', {})
        sim_params = JSONToConfiguration(sim_params)
        if sim_params == {}:
            self.logger.info("Simulation parameters were not specified, running default template parameters")

        res = lsm_template.getSimulations(simulation_name=simulation_name, **sim_params)

        if len(res)==0:
            raise Exception("Simulation with associated parameters was not found")
        if len(res)>1:
            self.logger.warning("There are multiple simulations under the provided parameters, picking the first one")

        res = res[0]
        # getX returns dask operations, we pickle those operation to append tasks lazily from next nodes
        d_dask_tree = res.getDosage()
        c_dask_tree = res.getConcentration()
        d_file = self.save_dask_tree(project=p, dask_tree=d_dask_tree)
        c_file = self.save_dask_tree(project=p, dask_tree=c_dask_tree)
        
        return dict(dosageXarray=str(d_file), concentrationXarray=str(c_file))

