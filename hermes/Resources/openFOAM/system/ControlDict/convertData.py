class copyDataControlDict:

    def __init__(self):
        pass

    @staticmethod
    def updateDictionaryToJson(jsonTempalte, dictionaryData):
        for key, value in dictionaryData.items():
            jsonTempalte[key] = value
        return jsonTempalte