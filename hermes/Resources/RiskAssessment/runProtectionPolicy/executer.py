from ...executers.abstractExecuter import abstractExecuter


class runProtectionPolicy(abstractExecuter):
    """
        Runs a Fortran LSM simulation.

        inputs:
            ProjectName : str, The class path string to the class
            LSMDosage : str, path to file containing the dosage used in policy protection calculation
            LSMConcentration : str, path to file containing the concentration used in policy protection calculation
            policy : dict, dictionary of the policies to be applied
    """

    def _defaultParameters(self):
        return dict(
            output=[],

            inputs=["ProjectName","LSMDosage", "LSMConcentration", "policy"],
            webGUI={},
            parameters={}
        )

    @staticmethod
    def testParamValues(params: dict[str, any]):
        passed, status_message = abstractExecuter.checkParamType(params, "ProjectName", str, required=True)
        if not passed:
            return passed, status_message
        
        if abstractExecuter.isParamTestable(params, "ProjectName"):
            from hera.datalayer.project import getProjectList
            passed, status_message = abstractExecuter.checkParamAgainstList(params, "ProjectName", getProjectList(), False)
            if not passed:
                return passed, status_message
        
        passed, status_message = abstractExecuter.checkParamType(params, "policy", dict, required=True)
        if not passed:
            return passed, status_message
        
        if ("LSMDosage" in params) ^ ("LSMConcentration" in params):
            return False, "Protection policy calculation requires LSM simulation results path through `LSMConcentration` or `LSMDosage` parameter"

        for param in ["LSMDosage", "LSMConcentration"]:
            passed, status_message = abstractExecuter.checkParamType(params, param, str, required=False)
            if not passed:
                return passed, status_message
        
        return True, ""

    def run(self, **inputs):

        if 'ProjectName' not in inputs:
            raise Exception("Node wasn't given project name through `ProjectName` parameter")
        if 'policy' not in inputs:
            raise Exception("Node wasn't given the protection policy through `policy` parameter")

        from hera.datalayer import Project
        from hera.riskassessment import ProtectionPolicy
        from hera.simulations.LSM.singleSimulation import SingleSimulation

        p = Project(projectName=inputs['ProjectName'])
        if 'LSMDosage' in inputs:
            pickled_xarray, _ = self.load_xarray(inputs["LSMDosage"])

            conc = SingleSimulation(pickled_xarray).getConcentration()
        elif 'LSMConcentration' in inputs:
            conc, _ = self.load_xarray(inputs["LSMConcentration"])
        else:
            raise Exception("Node wasn't given LSM simulation results path through `LSMConcentration` or `LSMDosage` parameter")

        
        policy = ProtectionPolicy()

        policy_dict = inputs['policy']
        if not isinstance(policy_dict , dict):
            raise Exception("Protection policy must be dictionary of applied policies in the order of execution")
        
        policy.addActions({"actions":[{"name": policy_name, "params":policy_desc} for policy_name, policy_desc in policy_dict.items()]})

        res = policy.compute(conc, C="C", lazy=True)
        return dict(concentrationXarray=str(self.save_dask_tree(project=p, dask_tree=res)))