class copyDataControlDict:

    def __init__(self):
        pass

    @staticmethod
    def updateDictionaryToJson(jsonTemplate, dictionaryData):
        """
        Converts flat dictionaryData into the structured JSON expected by the controlDict Jinja template.
        """
        if "Execution" not in jsonTemplate:
            jsonTemplate["Execution"] = {}

        if "input_parameters" not in jsonTemplate["Execution"]:
            jsonTemplate["Execution"]["input_parameters"] = {}

        jsonTemplate["Execution"]["input_parameters"]["values"] = dictionaryData

        return jsonTemplate
