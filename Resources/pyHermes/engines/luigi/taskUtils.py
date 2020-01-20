from collections.abc import Iterable
import json
import jsonpath_rw_ext as jp

import pyHermes
class utils(object):

    def get_all_required_outputs(self):
        ret = {}
        for nodename, taskTarget in self.input().items():
            #print("Load %s" % taskTarget.fn)
            try:
                with open(taskTarget.fn) as jsoninput:
                    output = json.load(jsoninput)
            except json.JSONDecodeError:
                print("cannot open %s, return an empty map" % taskTarget.fn)
                output = {}

            #print("\t%s %s" %(nodename,output))
            #local = dict([("%s.%s" % (nodename, key), value) for key, value in output.items()])

            ret.update({nodename :output})
            #print(ret)
        return ret

    def _queryJSONPath(self, JSONPath):
        """
            Using the JSONPath module to query the

        :param JSONPath:
        :return:
        """
        res = [r for r in jp.match(JSONPath, self.taskJSON)]
        return res[0] if len(res) == 1 else res

    def _evaluate_path(self,
                       parampath,
                       params):
        """
        <parameter name> :  [Exp path],
                                        <node name>.[Node path].


                    [Exp path]  = <workflow|input|output|value|parameters|input_parameters|WebGUI|Properties|WebGui|>.[Exp path]
                    [Node Path] = <node name>.[Exp path|node path]


        :param parampath:
            The path of the parameter
        :param params:
            A dict of the parameters.
            The keys are [required nodes], workflow, parameters, WebGUI
        :return:
            The value of the parameter, str
        """
        path_tokens = parampath.split(".")

        func_name = path_tokens[0] if path_tokens[0] in ["WebGUI","parameters","workflow","input_parameters","output","Properties","WebGui"] else "node"
        func = getattr(self, "_handle_%s" % func_name)

        if len(path_tokens[1:]) == 0:
            raise ValueError("Some error with path: %s " % parampath)

        retval = func(".".join(path_tokens[1:]), params.get(path_tokens[0],{}))
        print("%s-->%s == %s" % (func_name, path_tokens[1:],retval))
        return retval

    def _handle_WebGUI(self, parameterPath, params):
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_parameters(self, parameterPath, params):
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_node(self, parameterPath, params):
        return self._evaluate_path(parameterPath,params)

    def _handle_workflow(self, parameterPath, params):
        retval = jp.match(parameterPath, self.workflowJSON)
        return retval if len(retval) > 1 else retval[0]

    def _handle_input_parameters(self, parameterPath, params):
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_output(self,parameterPath, params):
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_Properties(self,parameterPath, params):
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_WebGui(self,parameterPath, params):
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]


    def build_executer_parameters(self, task_executer_mapping, params):
        ret = {}
        for paramname, parampath in task_executer_mapping.items():

            if isinstance(parampath, str):
                #value = []
                value=""
                tokenList = pyHermes.hermesTaskWrapper.parsePath(parampath)
                for token,ispath in tokenList:
                    if ispath:
                        #value.append(self._evaluate_path(token, params))
                        value=self._evaluate_path(token, params)
                    else:
                        #value.append(token)
                        value=token
                #ret[paramname] = "".join(value)
                ret[paramname] =value

            elif isinstance(parampath, dict):
                param_ret = {}
                for dict_paramname, dict_parampath in parampath.item():
                    param_ret[dict_paramname] = self.build_executer_parameters(dict_parampath, params)

                ret[paramname] = param_ret
            elif isinstance(parampath, Iterable):
                param_ret = []
                for dict_parampath in parampath:
                    param_ret.append(self.build_executer_parameters(dict_parampath, params))

                ret[paramname] = param_ret

        return ret



