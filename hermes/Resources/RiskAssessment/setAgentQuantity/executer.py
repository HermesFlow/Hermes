from ...executers.abstractExecuter import abstractExecuter


class setAgentQuantity(abstractExecuter):
    """
        Set the quantity released in an LSM simulation

        inputs:
            ProjectName : str, name of the project to use
            LSMDosage : str, path to file containing the dosage used in policy protection calculation
            LSMConcentration : str, path to file containing the concentration used in policy protection calculation
            Quantity : str, Quantity of agent released and must specify units(500*kg)
            MassUnits : str, the units to use in the xarray for mass(default is milligrams)
            TimeUnits : str, the units to use in the xarray for time(default is minutes)
    """

    def _defaultParameters(self):
        return dict(
            output=[],

            inputs=["ProjectName", "LSMDosage", "LSMConcentration", "Quantity", "MassUnits", "TimeUnits"],
            webGUI={},
            parameters={}
        )

    @staticmethod
    def testParamValues(params: dict[str, any]):        
        if ("LSMDosage" in params) ^ ("LSMConcentration" in params):
            return False, "Setting simulation's Quantity requires LSM simulation results path exclusively through `LSMConcentration` or `LSMDosage` parameter"

        for param in ["LSMDosage", "LSMConcentration"]:
            passed, status_message = abstractExecuter.checkParamType(params, param, str, required=False)
            if not passed:
                return passed, status_message
 
        passed, status_message = abstractExecuter.checkParamType(params, "Quantity", (str), required=True)
        if not passed:
            return passed, status_message

        passed, status_message = abstractExecuter.checkParamType(params, "MassUnits", str, required=False)
        if not passed:
            return passed, status_message
        
        passed, status_message = abstractExecuter.checkParamType(params, "TimeUnits", str, required=False)
        if not passed:
            return passed, status_message
        
        return True, ""

    def run(self, **inputs):
        from hera.datalayer import Project
        from hera.utils.unitHandler import ureg
        from pint import set_application_registry
        set_application_registry(ureg)


        if 'ProjectName' not in inputs:
            raise Exception("Node wasn't given project name through `ProjectName` parameter")
        p = Project(projectName=inputs['ProjectName'])

        if 'LSMDosage' in inputs:
            xarr, _ = self.load_xarray(inputs["LSMDosage"])
        elif 'LSMConcentration' in inputs:
            xarr, _ = self.load_xarray(inputs["LSMConcentration"])
        else:
            raise Exception("Node wasn't given LSM simulation results path through `LSMConcentration` or `LSMDosage` parameter")

        if 'Quantity' not in inputs:
            raise Exception("Node wasn't given Quantity though the `Quantity` parameter")
        quantity = inputs['Quantity']
        if not isinstance(quantity, str):
            raise Exception("Quantity must be a string specifying quantity of agent in units")
        mass_units = inputs.get('MassUnits', "kg")
        if not isinstance(mass_units, str):
            raise Exception("MassUnits must be a string specifying mass units to use in xarray")
        time_units = inputs.get('TimeUnits', "kg")
        if not isinstance(time_units, str):
            raise Exception("TimeUnits must be a string specifying time units to use in xarray")
        
        
        
        quantity = ureg.parse_expression((quantity))
        mass_units = ureg.parse_units(mass_units)
        time_units = ureg.parse_units(time_units)


        from numpy import timedelta64
        from pandas.api.types import is_numeric_dtype

        if 'dt' not in xarr.attrs: # xarray doesn't have LSM simulation dosage attributes
            if is_numeric_dtype(xarr.datetime.dtype):
                dt_minutes = xarr.datetime.isel(datetime=[0,1]).diff('datetime')[0].values.item()*ureg.sec
            else:
                dt_minutes = (xarr.datetime.isel(datetime=[0,1]).diff('datetime')[0].values / timedelta64(1, 'm')) * ureg.min

            xarr.attrs['dt'] = dt_minutes.to(time_units)
            xarr.attrs['Q']  = quantity.to(mass_units)
            xarr.attrs['C']  = 1*mass_units/ ureg.m ** 3
            dosage_factor = (quantity.to(mass_units) * ureg.min / ureg.m ** 3).m_as(mass_units * time_units / ureg.m ** 3)
            conc_factor = (quantity.to(mass_units) / ureg.m ** 3).m_as(mass_units / ureg.m ** 3)
        else:
            previous_dosage_factor = (xarr.attrs['Q'] * ureg.min / ureg.m ** 3).m_as(xarr.attrs['Q'].units * xarr.attrs['dt'].units / ureg.m ** 3)
            new_dosage_factor = (quantity.to(mass_units) * ureg.min / ureg.m ** 3).m_as(mass_units * time_units / ureg.m ** 3)
            dosage_factor = new_dosage_factor/previous_dosage_factor
            
            previous_conc_factor = (xarr.attrs['Q'] / ureg.m ** 3).m_as(xarr.attrs['Q'].units / ureg.m ** 3)
            new_conc_factor = (quantity.to(mass_units) / ureg.m ** 3).m_as(mass_units / ureg.m ** 3)
            conc_factor = new_conc_factor/previous_conc_factor
            xarr.attrs['dt'] = xarr.attrs['dt'].to(time_units)
            xarr.attrs['Q']  = quantity.to(mass_units)
            xarr.attrs['C']  = 1*mass_units/ ureg.m ** 3
        if "LSMDosage" in inputs:
            xarr['Dosage'] = dosage_factor*xarr['Dosage']
        elif "LSMConcentration" in inputs:
            if 'dDosage' in xarr:
                xarr['dDosage'] = dosage_factor*xarr['dDosage']
            xarr['C'] = conc_factor*xarr['C']


        return dict(xarray=str(self.save_dask_tree(project=p, dask_tree=xarr)))