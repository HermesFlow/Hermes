from ...executers.abstractExecuter import abstractExecuter


class weightedSumSimulation(abstractExecuter):
    """
        Set the quantity released in an LSM simulation

        inputs:
            ProjectName : str, name of the project to use
            LSMConcentrations : list[str], list of concentration xarrays
            Weights : list[int], list of weights
    """

    def _defaultParameters(self):
        return dict(
            output=[],

            inputs=["ProjectName", "LSMConcentrations", "LSMDosages", "Weights"],
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
            

        if ("LSMDosages" in params) ^ ("LSMConcentrations" in params): # xor of both params
            return False, "weighted sum requires LSM simulation result paths exclusively through `LSMConcentrations` or `LSMDosages` parameter"
        
        passed, status_message = abstractExecuter.checkParamType(params, "LSMConcentrations", list, required=False)
        if not passed:
            return passed, status_message
 
        passed, status_message = abstractExecuter.checkParamType(params, "LSMDosages", list, required=False)
        if not passed:
            return passed, status_message
 
        passed, status_message = abstractExecuter.checkParamType(params, "Weights", list, required=True)
        if not passed:
            return passed, status_message
        
        if abstractExecuter.isParamTestable(params, "Weights"):
            if all([((not abstractExecuter.isParamTestable(params["Weights"], i)) or isinstance(weight, (int,float)))
                    for i, weight in enumerate(params["Weights"])]):
                return False, "All weights must be numbers"
            
            if abstractExecuter.isParamTestable(params, "LSMConcentrations"):
                if len(params["LSMConcentrations"]) != len(params["Weights"]):
                    return False, "The list of simulations and weights must be equal in length"

                if all([isinstance(lsmConc, str) for lsmConc in params["LSMConcentrations"]]):
                    return False, "All simulation concentration paths must be strings"
                
            if abstractExecuter.isParamTestable(params, "LSMDosages"):
                if len(params["LSMDosages"]) != len(params["Weights"]):
                    return False, "The list of simulations and weights must be equal in length"

                if all([isinstance(lsmConc, str) for lsmConc in params["LSMDosages"]]):
                    return False, "All simulation dosage paths must be strings"

        
        return True, ""

    def run(self, **inputs):
        from hera.datalayer import Project

        if 'ProjectName' not in inputs:
            raise Exception("Node wasn't given project name through `ProjectName` parameter")
        p = Project(projectName=inputs['ProjectName'])

        if ("LSMDosages" in inputs) ^ ("LSMConcentrations" in inputs): # xor of both params
            return Exception("weighted sum requires LSM simulation result paths exclusively through `LSMConcentrations` or `LSMDosages` parameter")
        if 'LSMDosages' in inputs:
            xarrs, _ = self.load_xarray(inputs["LSMDosages"])
        elif 'LSMConcentrations' in inputs:
            xarrs, _ = self.load_xarray(inputs["LSMConcentrations"])
        else: # can't reach here, sanity check
            raise Exception("Node wasn't given LSM simulation results path through `LSMConcentrations` or `LSMDosages` parameter")
        
        if 'Weights' in inputs:
            weights, _ = self.load_xarray(inputs["Weights"])
        else: # can't reach here, sanity check
            raise Exception("Node wasn't given weights through `Weights` parameter")
        
        xarr = sum(ds*weight for ds, weight in zip(xarrs, weights))
        
        return dict(xarray=str(self.save_dask_tree(project=p, dask_tree=xarr)))