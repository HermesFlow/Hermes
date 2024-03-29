# import FreeCAD modules
import FreeCAD, FreeCADGui, WebGui
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

    import PySide
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *


# python modules
from PyQt5 import QtGui,QtCore
import json
import pydoc
import os
import sys
import copy

# Hermes modules
# from hermes.Resources.workbench.HermesNode import WebGuiNode
from ....workbench.HermesNode import WebGuiNode
from ....workbench.HermesNode import HermesNode as C_HermesNode
from ....workbench import HermesNode
from ....BC import workbench as BCworkbench


# import HermesGeometryDefinerEntity
# import HermesPart
from ..GeometryDefiner.workbench import GeometryDefinerNode

# =============================================================================
# BlockMeshNode
# =============================================================================
class BlockMeshNode(GeometryDefinerNode):
    '''
        the  class inherited from GeometryDefinerNode -
            - use same functionality
            - update differnt structure of json
    '''

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)
        self.initBMflag = False
        self.BMcount = 0

    def initializeFromJson(self, obj):
        '''
            Creates BlockMesh entities from json
        '''
        C_HermesNode.initializeFromJson(self, obj)

        # additional initialization BlockMesh node
        # ! not uploading parts at the moment !
        # self.linkPartToBM(obj)

        # get Geometry Face types section from json
        GeometryFaceTypes = self.nodeData["GeometryFaceTypes"]

        # get the list of available Geometry Face types
        TypeList = GeometryFaceTypes["TypeList"]

        # get the list of Geometry Entities that has been saved
        # boundaryList = self.nodeData["boundary"]
        # to make sure entities are not uploaded from json
        boundaryList = []

        # Loop all the Geometry Entities that has been saved (BME = BlockMeshEntity )
        for boundary in boundaryList:

            # Create the BME node
            from ..GeometryDefiner import workbenchEntity
            BMENodeObj = workbenchEntity.makeEntityNode('BME', TypeList, boundary, obj)
            if BMENodeObj is None:
                return None

            # get the GE properties, and update their current value
            GEProperties = boundary["Properties"]
            BMENodeObj.Proxy.setCurrentPropertyGE(BMENodeObj, GEProperties)

            # Update the faces attach to the BME (also create the parts)
            BMENodeObj.Proxy.initFacesFromJson(BMENodeObj)

            # get BME Name and update his Label property
            BMEName = boundary["Name"]
            BMENodeObj.Label = BMEName

            # get BME type and update his Type property
            BMEType = boundary["Type"]
            BMENodeObj.Type = BMEType

    def doubleClickedNode(self, obj):
        '''
            open one of 2 dialog panels:
            1. in case partLink hasn't been defined - open a dialog that
               give a list of FreeCAD parts, to choose one part.
            2. partLink exist -> open the Geometry definer dialog,
                allow only faces from the part that is linked
        '''

        partLink = getattr(obj, "partLink")

        if partLink is not None:
            # continue to usual GeometryDefiner
            super().doubleClickedNode(obj)

        else:
            # open Dialog to define part Link - when it is not defined

            # create CGEDialogPanel Object
            blockMeshGeDialog = BlockMeshGeometryLinkDialogPanel(obj)

            # get Parts from FC
            Parts = [FCobj.Label for FCobj in FreeCAD.ActiveDocument.Objects if FCobj.Module == 'Part']

            # in case part list is empty -> no need dialog
            if len(Parts) == 0:
                FreeCAD.Console.PrintWarning("There are no geometries in FreeCAD document, or all have been defined \n")
                return

            # add the part to options at the dialog
            for part in Parts:
                blockMeshGeDialog.addGemotry(part)

            # update the first value to be shown in the comboBox
            blockMeshGeDialog.setCurrentGeometry(Parts[0])

            # add node Object name to the geDialog name
            blockMeshGeDialog.setCallingObject(obj.Name)

            # show the Dialog in FreeCAD
            FreeCADGui.Control.showDialog(blockMeshGeDialog)





    def BlockMeshGeDialogClosed(self, obj, geometryLabel):
        '''
            update data from Dialog in FreeCAD object
        '''

        geometryObj = FreeCAD.ActiveDocument.getObjectsByLabel(geometryLabel)[0]
        setattr(obj, "partName", geometryObj.Name)
        setattr(obj, "partLink", geometryObj)

        # todo - if neighbourPatch name updated, update in eighbour
        # if getattr(obj, "Type") == "cylclic":



    def linkPartToBM(self, obj):
        '''
            not in use
            if part was uploaded through json, allow to link it to the node
        '''

        # get the part name and path
        partPath = getattr(obj, "partPath")
        partName = getattr(obj, "partName")

        if len(partPath) != 0 and len(partName) != 0:

            # Create full path of the part for Import
            pathPartStr = partPath + partName + ".stp" if list(partPath)[
                                                              -1] == '/' else partPath + "/" + partName + ".stp"
            # get workflow obj
            workflowObj = obj.getParentGroup()

            # create the part
            # partNameFC = workflowObj.Proxy.loadPart(workflowObj, pathPartStr)
            partNameFC = ""

            # make sure part imported
            if len(partNameFC) != 0:

                # get part by its name in FC
                partObj = FreeCAD.ActiveDocument.getObject(partNameFC)

                # update the part Name at the BlockMesh node properties
                setattr(obj, "partName", partNameFC)

                # link the part to thr BlockMesh node
                setattr(obj, "partLink", partObj)

                # flag for linking from json
                self.initBMflag = True

                # link the part to BM children
                for child in obj.Group:
                    # set the BlockMesh partlink  at each child
                    setattr(child, "partLink", partObj)
            else:
                FreeCAD.Console.PrintWarning(
                    'BlockMesh part has not been uploaded - check path and/or name of the part\n')
        else:
            FreeCAD.Console.PrintWarning('path or name of the BlockMesh part is missing\n')

    def backupNodeData(self, obj):
        '''
            update data from FreeCAD object to json
            specific:
            - vertices of the part that is linked to the node
            - boundary: list of blockMesh entities
        '''
        # super().backupNodeData(obj)
        for child in obj.Group:
            child.Proxy.UpdateFacesInJson(child)

        # get workflow object
        workflowObj = obj.getParentGroup()

        # get part object
        partObj = getattr(obj, "partLink")
        if partObj is not None:
            # get the part dictionary with and vertices data
            partName = partObj.Name

            # if partName not in workflowObj.Proxy.partList:
            from .. import workbenchPart
            workflowObj.Proxy.partList[partName] = workbenchPart.HermesPart(partName).getpartDict()

            partDict = workflowObj.Proxy.partList[partName]
            vertices = partDict["Vertices"]["openFoam"]

            # export BM partand json - do no export part here
            # remove connection part
            # workflowObj.Proxy.ExportPart(partName)

            # update vertices in nodedata
            self.updateVertices(vertices)

        # update boundary in nodedata
        self.updateBoundary(obj)

        # Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def updateBoundary(self, obj):
        ''' save the children(BlockMesh entities) nodes data into json'''
        # initialize boundary list
        boundaryList = []

        # loop all objects in Nodeobj
        for child in obj.Group:
            # get GE-child nodeDate from EntityNodeDataString property
            BMEnodeData = json.loads(child.EntityNodeDataString)

            # update the GE-child nodeDate in the Geometry Entity List section
            boundaryList.append(BMEnodeData)

        # update the Geometry Entity List section data in nodeData
        self.nodeData['boundary'] = boundaryList

    def updateVertices(self, vertices):
        '''create a list of string vertices'''

        ListVertices = []
        for ver in vertices:
            # string = self.createVerticesString(vertices[ver])
            # ListVertices.append(string)

            listVer = self.createVerticesList(vertices[ver])
            ListVertices.append(listVer)

        # push the list to the form data
        self.nodeData['vertices'] = ListVertices

    def createVerticesList(self,ver):
        listVer = list()
        for cor in ver['coordinates']:
            listVer.append(ver['coordinates'][cor])

        return listVer

    def createVerticesString(self, ver):
        string = ""
        for cor in ver['coordinates']:
            string += str(ver['coordinates'][cor]) + " "

        return string

    def UpdateNodePropertiesData(self, obj):
        ''' update propertis data from FreeCAD to json, also children nodes'''

        # get workflow object
        workflowObj = obj.getParentGroup()

        # update part path
        if workflowObj.ExportGUIJSONFile:
            setattr(obj, "partPath", workflowObj.ExportGUIJSONFile)
        else:
            setattr(obj, "partPath", workflowObj.ExportExecuteJSONFile)

        # update properties as parent
        C_HermesNode.UpdateNodePropertiesData(self, obj)

        # update children propeties
        for child in obj.Group:
            # update current properties value of the GE-child
            child.Proxy.UpdateGENodePropertiesData(child)

    def guiToExecute(self, obj):
        '''
            convert the json data to "inputParameters" structure
        '''

        # geometry
        simpleGrading = []
        json_grading = [getattr(obj, "simpleGradingX"), getattr(obj, "simpleGradingY"), getattr(obj, "simpleGradingZ")]
        grading = []
        for cor in json_grading:
            sg_list = []
            for sg in cor:
                if len(sg.split()) == 1:
                    item = float(sg)
                    sg_list.append(item)
                else:
                    item = [float(e) for e in sg.split()]
                    sg_list.append(item)

            grading.append(sg_list)

        # FreeCAD.Console.PrintMessage("grading = " + str(grading) + "\n")

        cellCount = [int(c) for c in getattr(obj, "NumberOfCells").split()]
        convertToMeters = int(getattr(obj, "convertToMeters"))

        geometry = dict(convertToMeters=convertToMeters, cellCount=cellCount, grading=grading)

        # vertices
        vertices = self.nodeData["vertices"]
        # json_vertices = self.nodeData["vertices"]
        # vertices = list()
        # for ver in json_vertices:
        #     l_ver = ver.split()
        #     vertices.append(l_ver)

        # boundary
        json_boundary = self.nodeData["boundary"]
        boundary = list()
        for bn in json_boundary:
            bn_dict = dict()
            bn_dict["name"] = bn["Name"]
            bn_dict["type"] = bn["Type"]
            bn_dict["faces"] = [bn["faces"][face]["vertices"] for face in bn["faces"]]
            if bn["Type"] == "cyclic":
                bn_dict["neighbourPatch"] = bn["Properties"]["neighbourPatch"]["current_val"]

            boundary.append(copy.deepcopy(bn_dict))



        jinja = dict(geometry=geometry, boundary=boundary, vertices=vertices)
        # FreeCAD.Console.PrintMessage("blockMesh guiToExecute = " + str(jinja) + "\n")

        return jinja

    def executeToGui(self, obj, parameters):
        ''' import the "input_parameters" data into the json obj data '''

        # update the geometry section in FC properties
        geometry = parameters["geometry"]
        if len(geometry) > 0:
            # FreeCAD.Console.PrintMessage("geometry = " + str(geometry) + "\n")
            setattr(obj, "convertToMeters", geometry["convertToMeters"])
            cellCountStr = " ".join(map(str, geometry["cellCount"]))
            setattr(obj, "NumberOfCells", cellCountStr)

            # if grade consist of 1 list -> convert to arr with 1 str
            # if grade consist of 3 lists-> loop each list, convert to arr with 3 str
            simpleGrading = list()
            for grade in geometry["grading"]:
                if len(grade) == 1:
                    simpleGrading.append([" ".join(map(str, grade))])
                else:
                    subSimpleGrading = list()
                    subIdx = 0
                    for subGrade in grade:
                        subSimpleGrading.append(" ".join(map(str, subGrade)))
                    # simpleGrading[idx] = subSimpleGrading
                    simpleGrading.append(subSimpleGrading)

            # update the data in FC obj
            setattr(obj, "simpleGradingX", simpleGrading[0])
            setattr(obj, "simpleGradingY", simpleGrading[1])
            setattr(obj, "simpleGradingZ", simpleGrading[2])


        # FreeCAD.Console.PrintMessage("grading = " + str(grading) + "\n")



        # check that boundry box data(vertices) exist
        if len(parameters["vertices"]) == 0:
            return

        maxmin = {'min': 1e6, 'max': -1e6}
        extrema = [maxmin.copy(), maxmin.copy(), maxmin.copy()]
        for vertex in parameters["vertices"]:
            for i in range(len(vertex)):
                if vertex[i] < extrema[i]["min"]:
                    extrema[i]["min"] = vertex[i]
                elif vertex[i] > extrema[i]["max"]:
                    extrema[i]["max"] = vertex[i]

        # create FreeCAD box part
        blockMeshCube = FreeCAD.ActiveDocument.addObject("Part::Box","Box")
        FreeCAD.ActiveDocument.ActiveObject.Label = "BlockMeshCube"
        FreeCAD.ActiveDocument.recompute()
        # x direction
        blockMeshCube.Length = extrema[0]["max"] - extrema[0]["min"]
        # y direction
        blockMeshCube.Width = extrema[1]["max"] - extrema[1]["min"]
        # z direction
        blockMeshCube.Height = extrema[2]["max"] - extrema[2]["min"]

        # create vector of the position of the cube
        position_vector = FreeCAD.Base.Vector(extrema[0]["min"], extrema[1]["min"], extrema[2]["min"])
        # move the cube to that location
        blockMeshCube.Placement.move(position_vector)


        # link the part to thr BlockMesh node
        setattr(obj, "partLink", blockMeshCube)

        # create the part object from the part
        self.backupNodeData(obj)

        # create BlockEntities based on the boundary input
        # get Geometry Face types section from json
        GeometryFaceTypes = self.nodeData["GeometryFaceTypes"]

        # get the list of available Geometry Face types
        TypeList = GeometryFaceTypes["TypeList"]


        if len(parameters["boundary"]) == 0:
            return

        for bound in parameters["boundary"]:
            # Create basic structure of a GENodeData
            Properties = GeometryFaceTypes["TypeProperties"][bound["type"]]["Properties"]
            BmNodeData = dict(Name=bound["name"], Type=bound["type"], Properties=Properties)
            faceList = bound["faces"]

            # update the Reference(faces) list attach to the the BMEObj -
            for face_vertices in faceList:
                freecad_face = self.find_face_Name(obj, face_vertices, blockMeshCube.Name)
                if freecad_face is not None:
                    tmp = (blockMeshCube.Name, freecad_face)  # Reference structure
                    obj.References.append(tmp)


            # create the object
            from ..GeometryDefiner import workbenchEntity
            BmNodeObj = workbenchEntity.makeEntityNode(bound["name"], TypeList, copy.deepcopy(BmNodeData), obj)
            if BmNodeObj is None:
                return None

            # copy the Refernces list to the new BME object, and reset BM Refernces
            BmNodeObj.References = obj.References
            obj.References = []




    def find_face_Name(self, obj, faceVertices, partName):

        # get the part linked dictionary
        workflowObj = obj.getParentGroup()
        partDict = workflowObj.Proxy.partList[partName]
        OF_Faces = partDict["Faces"]

        # loop face till vertices are are equal
        for of_face in OF_Faces:
            if faceVertices == OF_Faces[of_face]["vertices"]:
                return of_face

        return None



# =============================================================================
# BlockMeshGeometryLinkDialogPanel
# =============================================================================
# Path To GE UI
blockMesh_ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
path_to_blockMeshGe_ui = blockMesh_ResourceDir + "Mod/Hermes/Resources/ui/blockmeshgeometry.ui"

class BlockMeshGeometryLinkDialogPanel:
    ''' The dialog class allow to choose a part to link to BlockMesh node'''

    def __init__(self, obj):
        # Create widget from ui file
        self.form = FreeCADGui.PySideUic.loadUi(path_to_blockMeshGe_ui)

    def addGemotry(self, gemetry):
        # add  geType to options at GE dialog
        self.form.m_pGeometryBM.addItem(gemetry)

    def setCurrentGeometry(self,GemetryName):
        # update the current value in the comboBox
        self.form.m_pGeometryBM.setCurrentText(GemetryName)

    def setCallingObject(self, callingObjName):
        # get obj Name, so in def 'accept' can call the obj
        self.callingObjName = callingObjName

    def accept(self):
        # Happen when Close Dialog
        # get the current GE type name from Dialog
        Geometry = self.form.m_pGeometryBM.currentText()

        # calling the nodeObj from name
        callingObject = FreeCAD.ActiveDocument.getObject(self.callingObjName)

        # calling the function that create the new GE Object
        callingObject.Proxy.BlockMeshGeDialogClosed(callingObject, Geometry)

        # # close the Dialog in FreeCAD
        FreeCADGui.Control.closeDialog()


    def reject(self):
        # check if it reset choices
        return True