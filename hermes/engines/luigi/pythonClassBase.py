import jinja2

class transform:
    """
        Transforms a TaskWrapper to the appropriate Luigi class.

        The default transformer assumes that all the parameters are
        either passed in the target output of the requierd task or
        hard coded in the workflow.

                    <parameter name> :  "string1 {[Exp path]|<node name>.[Node path]} string2 ..."


                    [Exp path]  = <JSON|input|output|input_parameters|parameters|WebGUI>.[Exp path]
                    [Node Path] = <node name>.[Exp path|node path]

    """

    _basicLuigiTemplate = """
class {{taskwrapper.taskfullname}}(luigi.Task,hermesutils):

    _taskJSON = None
    _workflowJSON = None 
    
    @property 
    def workflowJSON(self):
        return self._workflowJSON
        
    @property 
    def taskJSON(self):
        return self._taskJSON
    
    def __init__(self,*args,**kwargs): 
        super().__init__(*args,**kwargs)
        self._taskJSON ={}
        
        self._workflowJSON = {{taskwrapper.task_workflowJSON}}['workflow']

    def output(self):
        targetBaseFile = os.path.abspath(__file__).split(".")[0]
        return luigi.LocalTarget(os.path.join(f"{targetBaseFile}_targetFiles","{{taskwrapper.taskfullname}}.json"))

    def requires(self):
        return dict({% for (i,(rtaskname,rtask)) in enumerate(taskwrapper.requiredTasks.items()): %}
                       {{rtaskname}}={{rtask.taskfullname}}(){% if i+1<len(taskwrapper.requiredTasks) %},{% else %}{% endif %}{% endfor %}
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {{taskwrapper.input_parameters}}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        
        # We seperated the GUI from the execution. 
        # params['formData']   = {{taskwrapper.formData}}
        # params['files']      = {{taskwrapper.files}}
        # params['Schema']     = {{taskwrapper.Schema}}
        # params['uiSchema']   = {{taskwrapper.uiSchema}}
        # params['Properties'] = {{taskwrapper.task_Properties}}
        # params['WebGui']     = {{taskwrapper.task_webGui}}
        
       
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='{{WD_path}}'
                    
        from {{taskwrapper.getExecuterPackage()}} import {{taskwrapper.getExecuterClass()}}  
        output = {{taskwrapper.getExecuterClass()}}(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)
"""

    def transform(self,taskWrapper,WD_path):
        """
            Transforms a taskWrapper to a luigi task.

            The target class looks like this:

            <assumes that the class
                    import json


            class <full node name>(luigi.Task):

                def output(self):
                    return luigi.LocalTarget("<full node name>.json")

                def requires(self):

                    return { <node name> : <full node name>(),
                                        .  \
                                        .   The required tasks.
                                        .  /
                            <node name> : <full node name>() }


                def run(self):

                    import <executer full path>
                    executer = <executer full path>()

                    parameters_from_required = self.get_all_required_outputs()

                    executer_parameters = {
                            <parameter name> : <value from WebGUI, Parameters or workflowJSON>
                            <node parameter name> : parameters_from_required[node path]
                    }

                    output = executer(**executer_parameters)

                    ## now prepare the output:
                    outputmap = {
                            <parameters from taskJSON>
                            <WebGUI from taskJSON>
                            < .. all the parameters from the JSON of the workflow that are referenced here ..>
                            + parameters_from_required
                    }

                    with open(self.output().fn,"w") as outfile:
                        json.dump(pretty params, outmap)


                def get_all_required_outputs(self):
                    ret = {}
                    for nodename,task in self.inputs():
                        output = json.loads(task.output().fn)
                        local = dict([("<nodename>.%s" % key,value) for key,value in output.items()])
                        ret = ret.update(local)

                    return ret

        :param taskWrapper:
        :return:
            A string of the Luigi Task.
        """
        rtemplate = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(self._basicLuigiTemplate)
        return rtemplate.render(taskwrapper=taskWrapper,enumerate=enumerate,len=len,WD_path=WD_path,)

