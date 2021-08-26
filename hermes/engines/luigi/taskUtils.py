from collections.abc import Iterable
import json
import jsonpath_rw_ext as jp

import hermes
class utils(object):

    def get_all_required_outputs(self):
        ret = {}
        for nodename, taskTarget in self.input().items():
            print("Load %s" % taskTarget.fn)
            try:
                with open(taskTarget.fn) as jsoninput:
                    output = json.load(jsoninput)
            except json.JSONDecodeError:
                print("cannot open %s, return an empty map" % taskTarget.fn)
                output = {}

            #print("\t%s %s" %(nodename,output))
            #local = dict([("%s.%s" % (nodename, key), value) for key, value in output.items()])

            ret.update({nodename :output})

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
        func_name = path_tokens[0] if path_tokens[0] in ["WebGUI","parameters","workflow","input_parameters","output","Properties","WebGui","value"] else "node"
        func = getattr(self, "_handle_%s" % func_name)

        if len(path_tokens[1:]) == 0:
            raise ValueError("Some error with path: %s " % parampath)
        #retval = func(".".join(path_tokens[1:]), params.get(path_tokens[0],{}))
        retval = func(path_tokens, params)
        #print("%s-->%s == %s" % (func_name, path_tokens[1:],retval))
        return retval

    def _handle_WebGUI(self, parameterPath, params):
        params = params.get(parameterPath[0],{})
        parameterPath = ".".join(parameterPath[1:])
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_parameters(self, parameterPath, params):
        params = params.get(parameterPath[0],{})
        parameterPath = ".".join(parameterPath[1:])
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_node(self, parameterPath, params):
        params = params.get(parameterPath[0],{})
        parameterPath = ".".join(parameterPath[1:])
        return self._evaluate_path(parameterPath,params)

    def _handle_workflow(self, parameterPath, params):
        parameterPath = ".".join(parameterPath[1:])
        retval = jp.match(parameterPath, self.workflowJSON)
        return retval if len(retval) > 1 else retval[0]

    def _handle_input_parameters(self, parameterPath, params):
        params = params.get(parameterPath[0],{})
        parameterPath = ".".join(parameterPath[1:])
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_output(self,parameterPath, params):
        # if len(parameterPath) == 1:
        #     params = params.get(parameterPath[0], {})
        #     return params
        # else:
        params = params.get(parameterPath[0],{})
        parameterPath = ".".join(parameterPath[1:])
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_Properties(self,parameterPath, params):
        params = params.get(parameterPath[0],{})
        parameterPath = ".".join(parameterPath[1:])
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_WebGui(self,parameterPath, params):
        params = params.get(parameterPath[0],{})
        parameterPath = ".".join(parameterPath[1:])
        retval = jp.match(parameterPath, params)
        return retval if len(retval) > 1 else retval[0]

    def _handle_value(self,parameterPath, params):
        return params.get(".".join(parameterPath[1:]),{})


    def _parseAndEvaluatePath(self, paramPath,params):
        value = []
        tokenList = hermes.hermesTaskWrapper.parsePath(paramPath)
        for token, ispath in tokenList:
            if ispath:
                try:
                    value.append(self._evaluate_path(token, params))

                except IndexError:
                    errMsg = f"The token {token} not found in \n {json.dumps(params, indent=4, sort_keys=True)}"
                    print(errMsg)
                    raise KeyError(errMsg)

                except KeyError:
                    errMsg = f"The token {token} not found in \n {json.dumps(params, indent=4, sort_keys=True)}"
                    print(errMsg)
                    raise KeyError(errMsg)
            else:
                value.append(token)

        if (all([isinstance(x, str) for x in value])):
            ret = "".join(value)
        else:
            ret = value[0]

        return ret

    def build_executer_parameters(self, task_executer_mapping, params):
        ret = {}
        for paramname, parampath in task_executer_mapping.items():
            if isinstance(parampath, str):
                ret[paramname] = self._parseAndEvaluatePath(parampath,params)

            elif isinstance(parampath, dict):
                param_ret = {}
                for dict_paramname, dict_parampath in parampath.items():
                    if isinstance(dict_parampath,dict):
                        param_ret[dict_paramname] = self.build_executer_parameters({dict_paramname:dict_parampath}, params)[dict_paramname]
                    elif isinstance(dict_parampath,str):
                        param_ret[dict_paramname] = self._parseAndEvaluatePath(dict_parampath, params)
                    else:
                        param_ret[dict_paramname] = dict_parampath

                ret[paramname] = param_ret

            elif isinstance(parampath, Iterable):
                param_ret = []
                for dict_parampath in parampath:
                    if isinstance(dict_parampath,dict):
                        param_ret.append(self.build_executer_parameters(dict_parampath, params))
                    else:
                        param_ret.append(dict_parampath)

                ret[paramname] = param_ret
            else:
                ret[paramname] = parampath
        return ret



