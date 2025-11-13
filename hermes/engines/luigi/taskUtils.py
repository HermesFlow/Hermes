import os.path
from collections.abc import Iterable
import json
import jsonpath_rw_ext as jp
import sys
import hermes
from ...utils.logging import get_classMethod_logger,get_logger
class utils:

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

        If the path is empty return {}

        :param parampath:
            The path of the parameter
        :param params:
            A dict of the parameters.
            The keys are [required nodes], workflow, parameters, WebGUI
        :return:
            The value of the parameter, str
        """
        logger = get_classMethod_logger(self,"_evaluate_path")
        logger.debug(f"Processing {parampath} with params {params}")
        if len(parampath) == 0:
            return '{}'
        path_tokens = parampath.split(".")
        func_name = path_tokens[0] if path_tokens[0] in ["WebGUI","parameters","workflow","input_parameters","output","Properties","WebGui","value"] else "node"
        func = getattr(self, "_handle_%s" % func_name)
        if len(path_tokens[1:]) == 0:
            logger.critical(f"_evaluate_path: Some error with path: <{parampath}>. Assuming its C++ code.")
            retval = None
        else:#retval = func(".".join(path_tokens[1:]), params.get(path_tokens[0],{}))
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

    def _handle_token_moduleName(self):
        return sys.argv[2]

    def _handle_token_calc(self):
        return "#calc "

    def _parseAndEvaluatePath(self, paramPath,params):
        logger = get_classMethod_logger(self,"_parseAndEvaluatePath")
        value = []
        if paramPath.startswith("#{"):
            ret = paramPath
        else:
            tokenList = hermes.hermesTaskWrapper.parsePath(paramPath)
            logger.debug(f"Inspecting the token list {tokenList}")
            for token, ispath in tokenList:
                logger.info(f"The token {token}")
                testIfTokenIsAHandler = False
                if token.startswith("#"):
                    if len(token[1:]) > 0:
                        testIfTokenIsAHandler = True if hasattr(self,f"_handle_token_{token[1:]}".strip()) else False
                    else:
                        testIfTokenIsAHandler = False
                logger.debug(f"The token {token} is a handler? {testIfTokenIsAHandler}. Is path? {ispath}")
                if testIfTokenIsAHandler:
                    try:
                        tknval_func = getattr(self,f"_handle_token_{token[1:]}".strip())
                        value.append(tknval_func())
                    except AttributeError:
                        existingTokens = ",".join([x for x in dir(self) if x.startswith("_handle_token_")])
                        raise ValueError(f"token: {token[1:]} does not exist. Available Tokens are: {existingTokens}")
                elif ispath:
                    try:
                        ret = self._evaluate_path(token, params)
                        ret = f'"{str(ret)}"' if isinstance(ret,dict) else ret
                        value.append(ret)
                    except IndexError:
                        errMsg = f"The token {token} not found in \n {json.dumps(params, indent=4, sort_keys=True)}"
                        print(errMsg)
                        raise KeyError(errMsg)

                    except KeyError:
                        errMsg = f"The token {token} not found in \n {json.dumps(params, indent=4, sort_keys=True)}"
                        print(errMsg)
                        raise KeyError(errMsg)
                else:
                    logger.debug(token)
                    value.append(token)

            if (all([isinstance(x, str) or isinstance(x, float) or isinstance(x, int)  for x in value])):
                ret = "".join([str(x) for x in value])
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
                    elif isinstance(dict_parampath,list):
                        newValueList = []
                        for value in dict_parampath:
                            if isinstance(value, str):
                                newValue = self._parseAndEvaluatePath(value, params)
                            elif isinstance(value, dict):  # or isinstance(value,list): leads to a bug.
                                newValue = self.build_executer_parameters(value, params)
                            else:
                                newValue = value

                            newValueList.append(newValue)
                        param_ret[dict_paramname] =newValueList
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



