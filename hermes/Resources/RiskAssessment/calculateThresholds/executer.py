from ...executers.abstractExecuter import abstractExecuter


class calculateThresholds(abstractExecuter):
    """
        Set the quantity released in an LSM simulation

        inputs:
            ProjectName : str, name of the project to use
            LSMConcentration : str, path to file containing the concentrations used to calculate thesholds
            Agent : str, name of the agent released
            Calculator : str, name of the threshold calculator to use, defined per agent
    """

    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=["ProjectName", "LSMConcentration", "Agent", "Calculator"],
            webGUI={},
            parameters={}
        )

    @staticmethod
    def testParamValues(params: dict[str, any]):    
        passed, status_message = abstractExecuter.checkParamType(params, "ProjectName", str, required=True)
        if not passed:
            return passed, status_message
        
        passed, status_message = abstractExecuter.checkParamType(params, "LSMConcentration", str, required=True)
        if not passed:
            return passed, status_message
                
        passed, status_message = abstractExecuter.checkParamType(params, "Agent", str, required=True)
        if not passed:
            return passed, status_message
        
        passed, status_message = abstractExecuter.checkParamType(params, "Calculator", str, required=True)
        if not passed:
            return passed, status_message
        
        if abstractExecuter.isParamTestable(params, "ProjectName"):
            from hera import toolkitHome
            from hera.datalayer.project import Project, getProjectList
            passed, status_message = abstractExecuter.checkParamAgainstList(params, "ProjectName", getProjectList(), False)
            if not passed:
                return passed, status_message

            p = Project(projectName=params['ProjectName'])    
            risk_tk = toolkitHome.getToolkit(toolkitHome.RISKASSESSMENT, projectName=p.projectName)
            passed, status_message = abstractExecuter.checkParamAgainstList(params, "Agent", risk_tk.listAgentsNames(), True)
            if not passed:
                return passed, status_message
            if abstractExecuter.isParamTestable(params, "Agent"):
                agent = risk_tk.getAgent(params["Agent"])
                passed, status_message = abstractExecuter.checkParamAgainstList(params, "Calculator", agent.effectNames, True)
                if not passed:
                    return passed, status_message
                
        
        return True, ""

    def run(self, **inputs):
        from hera import toolkitHome
        from hera.datalayer import Project
        from hera.utils.unitHandler import ureg
        from pint import set_application_registry
        set_application_registry(ureg)

        if 'ProjectName' not in inputs:
            raise Exception("Node wasn't given project name through `ProjectName` parameter")
        p = Project(projectName=inputs['ProjectName'])

        if 'LSMConcentration' not in inputs:
            raise Exception("Node wasn't given LSM simulation results path through `LSMConcentration` or `LSMDosage` parameter")

        if 'Agent' not in inputs:
            raise Exception("Node wasn't given agent name through `Agent` parameter")
        risk_tk = toolkitHome.getToolkit(toolkitHome.RISKASSESSMENT, projectName=p.projectName)
        agent = risk_tk.getAgent(inputs["Agent"])
        
        if 'Calculator' not in inputs:
            raise Exception("Node wasn't given calculator name through `Calculator` parameter")
        if inputs["Calculator"] not in agent.effectNames:
            raise Exception(f"Calculator {inputs['Calculator']} isn't defined for agent {agent}, choose one of: {', '.join(agent.effectNames)}")
        calculator = getattr(agent, inputs["Calculator"])

        from hera.datalayer import autocache
        
        @autocache.cacheFunction(projectName=p.projectName, returnDoc=True)
        def load_and_calc_region_of_injured(xarr_path):
            xarr, _ = self.load_xarray(xarr_path)
            return calculator.calculateRegionOfInjured(xarr, "C")
        _, doc = load_and_calc_region_of_injured(inputs["LSMConcentration"])

        return dict(xarray=doc.resource)