
# import FreeCAD modules
import FreeCAD,FreeCADGui
from ....workbench import HermesTools
from ....workbench.HermesTools import addObjectProperty

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

import json

import copy

from .. import workbenchCfdFaceSelectWidget
# from hermes.Resources.workbench.openFOAM2.mesh import HermesPart
from .. import workbenchPart

# import Draft
# from Draft import _Facebinder
from ..GeometryDefiner.workbenchEntity import HermesGE
# -----------------------------------------------------------------------#
# This enables us to open a dialog on the left with a click of a button #
# -----------------------------------------------------------------------#


# =============================================================================
# Hermes BlockMesh Entity class
# =============================================================================
class HermesBME(HermesGE):
    '''
        the  class inherited from HermesGE -
            - use same functionality
            - update differnt structure of json
    '''

    def __init__(self, obj, TypeList, EntityNodeData):
        super().__init__(obj, TypeList, EntityNodeData)
        self.Properties = self.EntityNodeData["Properties"]

    def initProperties(self, obj):
        ''' Add specific properties of BlockMesh '''
        super().initProperties(obj)

        Nodeobj = obj.getParentGroup()
        if Nodeobj.Name == "BlockMesh":
            # link part - link to 1 part - Inherite from parent BM
            addObjectProperty(obj, "partLink", getattr(Nodeobj, "partLink"), "App::PropertyLink", "part", "Link GE to part")
            obj.setEditorMode("partLink", 1)

        # if type cyclic - update the Enumeration list in neighbourPatch property for all cyclic types
        if obj.Type == "cyclic":

            # loop all BlockMesh children
            for BME in Nodeobj.Group:

                # get list of all cyclic type nodes
                cyclicList = [BME.Label for BME in Nodeobj.Group if BME.Type == "cyclic"]
                if len(cyclicList) > 0:

                    # check if the current entity is cyclic
                    if BME.Type == "cyclic":

                        # make sure neighbourPatch property is defined
                        if "neighbourPatch" in BME.PropertiesList:

                            # get the current value at the neighbourPatch enum
                            currentVal = BME.neighbourPatch

                            # remove the current entity from cyclicList - cannot be its own neighbourPatch
                            cyclicList.remove(BME.Label)

                            if len(cyclicList) > 0:
                                # update the list of neighbourPatch enum
                                BME.neighbourPatch = cyclicList

                                # if it is not the default value, update the current value in enum(keep value while changing the enum list)
                                if currentVal != "notSet":
                                    setattr(BME, "neighbourPatch", currentVal)





    def UpdateFacesInJson(self,obj):
        '''
            Take the data from FreeCAD objects and save it as a json
            1. take the part from "partLink" and get its data as faces and vertices
            2. loop the References property
                save the specific faces names and vertices of the specific ref
                into the json
        '''

        # create struct of face
        faceStruct = {"vertices": ""}

        # update properties
        self.UpdateBMENodePropertiesData(obj)

        # create basic structure of a boundary
        boundary_strc = {
            "Name": obj.Label,
            "Type": obj.Type,
            "Properties": self.Properties,
            "faces": {}
        }

        # get workflowObj
        Nodeobj = obj.getParentGroup()
        workflowObj = Nodeobj.getParentGroup()

        # get the part dictionary with faces and vertices data
        partObj = getattr(obj, "partLink")
        if partObj is not None:

            # get the part dictionary with faces and vertices data
            partName = partObj.Name
            if partName not in workflowObj.Proxy.partList:
                workflowObj.Proxy.partList[partName] = workbenchPart.HermesPart(partName).getpartDict()
            partDict = workflowObj.Proxy.partList[partName]


            # Loop all the References in the object
            for Ref in obj.References:
                # example Refernces structure : obj.References=[('Cube','Face1'),('Cube','Face2')]
                # example Ref structure :Ref=('Cube','Face1')

                # get Name of the face from Current Reference
                FaceName = Ref[1]  # face

                # get the vertices of the face and sav as a string
                verticesList = partDict["Faces"][FaceName]['vertices']
                # verticesString = ' '.join(verticesList)

                # add the vrtices to the current face struct
                # faceStruct["vertices"] = verticesString
                faceStruct["vertices"] = verticesList

                # add the current face struct to the boundry struct
                boundary_strc["faces"][FaceName] = faceStruct.copy()


        # update the date in the NodeData
        self.EntityNodeData = boundary_strc.copy()

        # Update GEnodeData  at the EntityNodeDataString by converting from json to string
        obj.EntityNodeDataString = json.dumps(self.EntityNodeData)



    def initFacesFromJson(self, obj):
        ''' not in use at the moment - allow import part into FC
            and update entity'''
        # get faceList attach to the GE from GEnodeData
        faceList = self.EntityNodeData["faces"]
        PartObj = getattr(obj, "partLink")

        if PartObj is None:
            return

        givenPartName = PartObj.Name

        # update the Reference(faces) list attach to the the BMEObj -
        for face in faceList:
            tmp = (givenPartName, face)  # Reference structure
            obj.References.append(tmp)

    def UpdateBMENodePropertiesData(self, obj):
        '''use the part function to update the values of property'''
        super().UpdateGENodePropertiesData(obj)

        # update the self var of proporties
        self.Properties = self.EntityNodeData["Properties"]




