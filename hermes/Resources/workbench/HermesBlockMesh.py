
import FreeCAD
import json

class HermesBlockMesh:
    '''
    This class will translate the date from the GeometryDefiner node into the
    BlockMesh nodes as JSON
    This will be dynamic mode - will update at any change of the GeometryDefiner node.
    '''
    def __init__(self):
        pass

    def updateJson(self, GEnode):

        # get the blockMesh formData
        blockMeshObj = FreeCAD.ActiveDocument.getObject('BlockMesh')
        nodeData = json.loads(blockMeshObj.NodeDataString)
        formData = nodeData["WebGui"]["formData"]

        # get the partList dict
        workflowObj = blockMeshObj.getParentGroup()
        partList = workflowObj.Proxy.partList
        if len(partList) == 0:
            return

        # get GeometryDefiner updated json nodeData
        GEnodaData = json.loads(GEnode.NodeDataString)
        # get GeometryDefiner name
        GEList = GEnodaData["GeometryEntityList"]


        # get the part dict from the list(saved as FC part Label)
        partLabel = formData["partName"]
        if partLabel in partList:
            partName = FreeCAD.ActiveDocument.getObjectsByLabel(partLabel)[0].Name
            partDict = partList[partLabel]
        else:
            print("Error blockMesh: the part " +partLabel+ " has bo boundary condition")
            return


        # get the list of the vertices and faces
        vertices = partDict["Vertices"]["openFoam"]
        faces = partDict["Faces"]

        # -------update vertices--------
        # create a list of string vertices
        stringVertices = []
        for ver in vertices:
            string = self.createVerticesString(vertices[ver])
            stringVertices.append(string)


        # push the list to the form data
        formData['vertices'] = stringVertices

        # -------update boundry--------
        formData['boundary'] = []
        # update boundry
        for GEkey,GEval in GEList.items():
            BlkMshGE = {}
            # update Name and Type
            BlkMshGE['name'] = GEval['Name']
            BlkMshGE['type'] = GEval['Type']

            # update faces coordinates in Blockmesh node
            GEfaces = []
            # get the list of the GeometryDefiner faces
            for p in GEval['faceList']:
                if GEval['faceList'][p]['Name'] == partName:
                    GEfaces = GEval['faceList'][p]['faces']

            # translate faceName into string of coordinates - for each face
            BlkMshGE['faces'] = []
            for i in range(len(GEfaces)):
                faceName = GEfaces[i]
                verticesList = faces[faceName]['vertices']
                verticesString = ' '.join(verticesList)
                BlkMshGE['faces'].append(verticesString)

            formData['boundary'].append(BlkMshGE)

        # update the data back in the node
        nodeData["WebGui"]["formData"] = formData
        blockMeshObj.NodeDataString = json.dumps(nodeData)
        workflowObj.Proxy.JsonObject["workflow"]["nodes"]["BlockMesh"] = nodeData
        # print(blockMeshObj.NodeDataString)



    def createVerticesString(self, ver):
        string =""
        for cor in ver['coordinates']:
            string += str(ver['coordinates'][cor]) + " "

        return string




