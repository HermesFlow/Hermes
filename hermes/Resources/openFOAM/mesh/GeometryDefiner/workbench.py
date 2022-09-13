# import FreeCAD modules
import FreeCAD, FreeCADGui, WebGui
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

    from PySide.QtGui import *
    from PySide.QtCore import *

import json


# Hermes modules
from ....workbench.HermesNode import HermesNode as C_HermesNode
# from ... import HermesNode
from ....BC import workbench as BCworkbench

#
from . import workbenchEntity
# import HermesPart

# =============================================================================
# #GeometryDefinerNode
# =============================================================================
class GeometryDefinerNode(C_HermesNode):
    ''' Define the GeometryDefiner node'''

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def initializeFromJson(self, obj):
        '''
            creates the GeometryDefiner entities from JSON
        '''
        super().initializeFromJson(obj)

        # get Geometry Face types section from json
        GeometryFaceTypes = self.nodeData["GeometryFaceTypes"]

        # get the list of available Geometry Face types
        TypeList = GeometryFaceTypes["TypeList"]

        # get the list of Geometry Entities that has been saved
        # GeometryEntityList = self.nodeData["GeometryEntityList"]
        # To make sure entities are not uploaded from json
        GeometryEntityList = []

        # Loop all the Geometry Entities that has been saved (GE = GeometryEntity )
        for y in GeometryEntityList:
            # get GE'num' object ; num =1,2,3 ...
            GEnum = GeometryEntityList[y]

            # get Name,Type and Properties of the GE
            GEName = GEnum["Name"]
            GEType = GEnum["Type"]

            # Create the GE node
            # from . import HermesGeometryDefinerEntity
            GENodeObj = workbenchEntity.makeEntityNode('GEtemp', TypeList, GEnum, obj)
            if GENodeObj is None:
                return None

            # get the GE properties, and update their current value
            GEProperties = GEnum["Properties"]
            GENodeObj.Proxy.setCurrentPropertyGE(GENodeObj, GEProperties)

            # Update the faces attach to the GE (also create the parts)
            GENodeObj.Proxy.initFacesFromJson(GENodeObj)

            # get GE Name and update his Label property
            GEName = GEnum["Name"]
            GENodeObj.Label = GEName

            # get GE type and update his Type property
            GEType = GEnum["Type"]
            GENodeObj.Type = GEType

    def doubleClickedNode(self, obj):
        '''
            activeated on doubleclick
            creates a new GeometryDefiner entity - open a dialog to so
        '''
        super().doubleClickedNode(obj)

        # from . import HermesGeometryDefinerEntity
        # create CGEDialogPanel Object
        geDialog = workbenchEntity.CGEDialogPanel(obj)

        # get GEtypes section from json
        GETypes = self.nodeData["GeometryFaceTypes"]

        # get the list of available GE types from GEtypes section
        TypeList = GETypes["TypeList"]

        # add the GE types to options at GE dialog
        for types in TypeList:
            geDialog.addGE(types)

        # update the first value to be showen in the comboBox
        geDialog.setCurrentGE(types[0])

        # add node Object name to the geDialog name
        geDialog.setCallingObject(obj.Name)

        # show the Dialog in FreeCAD
        if FreeCADGui.Control.activeDialog():
            FreeCADGui.Control.closeDialog()

        FreeCADGui.Control.showDialog(geDialog)


    def backupNodeData(self, obj):
        super().backupNodeData(obj)
        # Update faceList in GeometryEntityList section to each Geometry Entity node
        for child in obj.Group:
            child.Proxy.UpdateFacesInJson(child)

    def UpdateNodePropertiesData(self, obj):
        '''
            creates the list of geometryDefines entites, and update
            in the JSON
        '''
        super().UpdateNodePropertiesData(obj)

        # in case amount of GE has been changed
        # Create basic structure of a GeometryEntityList (string) in the length of Children's obj amount
        # structure example:
        # -- "GeometryEntityList":{
        # --     "GE1":{ },
        # --     "GE2":{ },
        # --     "GE3":{ }
        # --  }
        x = 1
        GEListStr = "{"
        for child in obj.Group:
            if (x > 1):
                GEListStr += ','
            childStr = '"GE' + str(x) + '":{}'
            GEListStr += childStr
            x = x + 1
        GEListStr += "}"

        # convert structure from string to json
        GeometryEntityList = json.loads(GEListStr)

        # loop all GE(Geometry Entities) objects in Nodeobj
        x = 1
        for child in obj.Group:
            # update current properties value of the GE-child
            child.Proxy.UpdateGENodePropertiesData(child)

            # get GE-child nodeDate from EntityNodeDataString property
            GEnodeData = json.loads(child.EntityNodeDataString)

            # get GE'node' object ; node =1,2,3 ...
            GEnode = 'GE' + str(x)

            # update the GE-child nodeDate in the Geometry Entity List section
            GeometryEntityList[GEnode] = GEnodeData

            x = x + 1

        # update the Geometry Entity List section data in nodeData
        self.nodeData['GeometryEntityList'] = GeometryEntityList

        # Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

        # # update properties of the current node(before updated only the children)
        # super().UpdateNodePropertiesData(obj)

    def geDialogClosed(self, obj, GEtype, GEname):
        '''
            Called when created new GE node and the dialog is closed
            Get the data from dialog, creates the entity and
            update the data at the entity and BC(if exist)
        '''

        # Create basic structure of a GENodeData
        GENodeData = {
            "Name": "",
            "Type": "",
            "Properties": {}
        }

        # get the GE Type available from Json, and their list of properties
        GETypes = self.nodeData["GeometryFaceTypes"]
        TypeList = GETypes["TypeList"]
        TypeProperties = GETypes["TypeProperties"]

        # take the properties of the choosen GEtype from dialog
        GEJsonType = TypeProperties[GEtype]
        GEProperties = GEJsonType["Properties"]

        # update values in GENodeData structure
        GENodeData["Name"] = GEname  # meaningful name is thr type
        GENodeData["Type"] = GEtype
        GENodeData["Properties"] = GEProperties

        # Create the GEObject
        # from . import HermesGeometryDefinerEntity
        GENodeObj = workbenchEntity.makeEntityNode('GEtemp', TypeList, GENodeData, obj)
        if GENodeObj is None:
            return None

        # get the References from the parent node to the the new GE child
        GENodeObj.References = obj.References
        GENodeObj.Proxy.geDialogClosed(GENodeObj, GEtype, GEname)

        # Empty the parent node References for further use
        obj.References = []

        bcObj = BCworkbench.getBoundaryConditionNode()
        # bcObj = FreeCAD.ActiveDocument.getObject("BoundaryCondition")
        if bcObj is not None:
            bcObj.Proxy.updateBCPartList(bcObj)

        return
    def guiToExecute(self, obj):
        '''
            convert the json data to "inputParameters" structure
        '''
        pass


# =============================================================================
# #_CommandGeometryDefinerSelection
# =============================================================================
class _CommandGeometryDefinerSelection:
    """ Geometry Definer selection command definition """

    def GetResources(self):
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[
                                                      -1] == '/' else FreeCAD.getResourceDir() + "/"
        icon_path = ResourceDir + "Mod/Hermes/Resources/icons/GeometryDefiner.png"
        # icon_path = os.path.join(CfdTools.get_module_path(), "Gui", "Resources", "icons", "physics.png")

        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("GeometryDefinerSelection", "Export Geometry Definer"),
                'Accel': "",
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("GeometryDefinerSelection", "Export Geometry Definer as obj")}

    def IsActive(self):
        GD = FreeCAD.ActiveDocument.getObjectsByLabel("GeometryDefiner")[0]
        if GD is not None:
            children = GD.Group
            if len(children) > 0:
                return True
            else:
                return False
        return False

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Choose export")

        # get GeometryDefiner FreeCAD object
        GD = FreeCAD.ActiveDocument.getObjectsByLabel("GeometryDefiner")[0]

        # add all GeometryDefiner objects to a list
        objs = []
        for child in GD.Group:
            objs.append(child)

        # create help cube
        h_cube = FreeCAD.ActiveDocument.addObject("Part::Box", "NoNameCube")
        # h_cube.Label = "NoNameCube"
        FreeCAD.ActiveDocument.recompute()
        # Add to objs list -> in case of 1 object will still exports in names
        objs.append(h_cube)

        # save file in wanted location
        self.save_obj_file(objs)

        #  remove help object
        FreeCAD.ActiveDocument.removeObject("NoNameCube")

        del objs

    def save_obj_file(self, objs):
        '''
            a button that export .obj files
            not in use at the moment
        '''
        import Mesh
        import re

        # what the dialog open dir - path
        # path = FreeCAD.ConfigGet("UserAppData")
        path = os.getcwd()

        try:
            SaveName = QFileDialog.getSaveFileName(None, QString.fromLocal8Bit("Save Geometry Definer as obj file"),
                                                   path,
                                                   "*.obj")  # PyQt4
        #                          "here the text displayed on windows" "here the filter (extension)"

        except Exception:
            SaveName, Filter = PySide.QtGui.QFileDialog.getSaveFileName(None, "Save Geometry Definer as obj file", path,
                                                                        "*.obj")  # PySide
        #       "here the text displayed on windows" "here the filter (extension)"

        if SaveName == "":  # if the name file are not selected then Abord process
            FreeCAD.Console.PrintMessage("Export obj file aborted" + "\n")
        else:  # if the name file are selected
            # remove unnecessary suffix if user added it
            if SaveName.endswith(".obj"):
                SaveName = re.sub('\.obj$', '', SaveName)

            FreeCAD.Console.PrintMessage(
                "Exporting file " + SaveName + ".obj" + "\n")  # text displayed to Report view (Menu > View > Report view checked)
            try:  # if error detected to export ...
                outpath = u"" + SaveName + ".obj"
                Mesh.export(objs, outpath)
            except Exception:  # if error detected to write
                FreeCAD.Console.PrintError(
                    "Error Exporting file " + "\n")  # detect error ... display the text in red (PrintError)


if FreeCAD.GuiUp:
    FreeCADGui.addCommand('GeometryDefinerSelection', _CommandGeometryDefinerSelection())
