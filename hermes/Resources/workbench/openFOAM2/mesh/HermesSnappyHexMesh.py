# import FreeCAD modules
import FreeCAD

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

    import PySide
    from PySide.QtGui import *
    from PySide.QtCore import *


# python modules
from PyQt5 import QtCore
import json
import os
import copy

# Hermes modules

from ...HermesNode import _WebGuiNode, _HermesNode
from ... import HermesNode



# =============================================================================
# #_SnappyHexMesh
# =============================================================================
class _SnappyHexMesh(_WebGuiNode):
    ''' The snappyHexMesh class'''

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

        # geometry_obj = HermesNode.makeNode("Geometry", obj, str(0), self.nodeData["Geometry"])
        # refinement_obj = HermesNode.makeNode("Refinement", obj, str(0), self.nodeData["Refinement"])

        # create all snappyHexMesh sub nodes - castellatedMeshControls, snapControls, addLayersControls, meshQualityControls,
        #   Geometry and Refinement
        for key, val in self.nodeData.items():
            if key != 'Type' and key != 'Properties' and key != 'WebGui':
                node_obj = HermesNode.makeNode(key, obj, str(0), val)


    # def doubleClickedNode(self, obj):
    #     super().doubleClickedNode(obj)


    def backupNodeData(self, obj):
        ''' update the data from FreeCAD(node and children) to json '''
        super().backupNodeData(obj)

        for child in obj.Group:
            child.Proxy.backupNodeData(child)
            self.nodeData[child.Name] = json.loads(child.NodeDataString)

        # then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def jsonToJinja(self, obj):
        ''' convert the json data to "inputParameters" structure '''
        jinjaObj = dict()

        jinjaObj["modules"] = copy.deepcopy(self.nodeData["WebGui"]["formData"]["modules"])

        for child in obj.Group:
            jinjaObj[child.Name] = child.Proxy.jsonToJinja(child)
        return jinjaObj

# =============================================================================
# #_SnappyHexMeshCastellatedMeshControls
# =============================================================================
class _SnappyHexMeshCastellatedMeshControls(_WebGuiNode):
    #    super().funcName(var1,var,2..) - allow to use the function of the Parent,
    #    and add current class functionalites

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def doubleClickedNode(self, obj):
        # super().doubleClickedNode(obj)
        self.updateJson(obj)
        self.selectNode(obj)
        obj.IsActiveObj = True


    def selectNode(self, obj):
        '''
            update the coordinates of snappy point from FreeCAD to webGui.formData
            (if point exist)
            then continue as any other webGui node when node is selected
        '''
        # check point exist
        snappyPoint = [obj for obj in FreeCAD.ActiveDocument.Objects if "locationInMesh" in obj.Label]
        if len(snappyPoint) > 0:
            snappyPoint = snappyPoint[0]
            x = format(float(snappyPoint.X), '.2f')
            y = format(float(snappyPoint.Y), '.2f')
            z = format(float(snappyPoint.Z), '.2f')

            locationString = "(" + x + " " + y + " " + z + ")"

            self.nodeData["WebGui"]["formData"]["locationInMesh"] = locationString
        # update Point coordinate

        #continue as webgui
        super().selectNode(obj)

    def backupNodeData(self, obj):
        ''' update the data from FreeCAD to json
            also the point snappy object data from FreeCAD'''
        # backup the data of the last node pressed
        super().backupNodeData(obj)

        self.updatePointFromWebgui()

        # then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def updateJson(self, obj):
        obj.NodeDataString = json.dumps(self.nodeData)


    def updatePointFromWebgui(self):
        ''' update the coordinates of the snappy point from webGui.formDate into the
            FreeCAD point object'''
        snappyPoint = [obj for obj in FreeCAD.ActiveDocument.Objects if "locationInMesh" in obj.Label]
        if len(snappyPoint) > 0:
            snappyPoint = snappyPoint[0]
        else:
            return

        coordinates = self.pointStringToArr()

        # FreeCAD.Console.PrintMessage("l_location = " + str(l_location) + "\n")
        # FreeCAD.Console.PrintMessage("coordinates = " + str(coordinates) + "\n")

        if len(coordinates) == 3:
            # snappyPoint = snappyPoint[0]
            snappyPoint.X = coordinates[0]
            snappyPoint.Y = coordinates[1]
            snappyPoint.Z = coordinates[2]

    def jsonToJinja(self, obj):
        ''' convert the json data to "inputParameters" structure '''
        coordinates = self.pointStringToArr()
        jinjaObj = copy.deepcopy(self.nodeData["WebGui"]["formData"])
        jinjaObj['locationInMesh'] = coordinates
        return jinjaObj

    def pointStringToArr(self):
        ''' split and create a list of the coordinates from the string '''
        locationString = self.nodeData["WebGui"]["formData"]["locationInMesh"]
        l_location = locationString.split(" ")
        coordinates = list()
        for item in l_location:
            if "(" in item:
                coordinates.append(item.replace("(", ""))
            elif ")" in item:
                coordinates.append(item.replace(")", ""))
            else:
                coordinates.append(item)

        return coordinates


# =============================================================================
# #_SnappyHexMeshRefinement
# =============================================================================
class _SnappyHexMeshRefinement(_WebGuiNode):
    ''' the class of Refinment - will be update in the future'''

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def jsonToJinja(self, obj):
        return dict(regions={})

    # def doubleClickedNode(self, obj):
    #     # super().doubleClickedNode(obj)
    #     self.selectNode(obj)

    # def backupNodeData(self, obj):
    #     # backup the data of the last node pressed
    #     # super().backupNodeData(obj)
    #
    #     # then Update nodeData  at the NodeDataString by converting from json to string
    #     obj.NodeDataString = json.dumps(self.nodeData)

# =============================================================================
# #_SnappyHexMeshGeometry
# =============================================================================
class _SnappyHexMeshGeometry(_HermesNode):
    '''The snappy geometry class'''

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def initializeFromJson(self, obj):
        super().initializeFromJson(obj)

        for itemKey, itemVal in self.nodeData["Entities"]["items"].items():
            l = len(obj.Group)
            GeoEntity_obj = HermesNode.makeNode(itemKey, obj, str(l), itemVal)

    def doubleClickedNode(self, obj):
        '''
            open dialog panel to create a new snappy geometry entity
            choose part from FreeCAD parts list and create snappy
            node that linked to the part
        '''
        super().doubleClickedNode(obj)

        # -------- panel dialog box  definitions --------------

        # create snappyGeDialog Object
        snappyGeDialog = SnappyHexMeshGeometryEntityDialogPanel(obj)

        # get Parts from FC
        Parts = [FCobj.Label for FCobj in FreeCAD.ActiveDocument.Objects if FCobj.Module == 'Part']

        # make sure part won't be chosen twice
        for child in obj.Group:
            part = FreeCAD.ActiveDocument.getObject(child.partLinkName)
            if part is not None:
                if part.Label in Parts:
                    Parts.remove(part.Label)


        # in case part list is empty -> no need dialog
        if len(Parts) == 0:
            FreeCAD.Console.PrintWarning("There are no geometries in FreeCAD document, or all have been defined \n")
            return

        # add the part to options at the dialog
        for part in Parts:
            snappyGeDialog.addGemotry(part)

        # update the first value to be shown in the comboBox
        snappyGeDialog.setCurrentGeometry(Parts[0])

        # add node Object name to the geDialog name
        snappyGeDialog.setCallingObject(obj.Name)

        # show the Dialog in FreeCAD
        FreeCADGui.Control.showDialog(snappyGeDialog)


    def backupNodeData(self, obj):
        ''' update the data from FreeCAD node to json '''
        super().backupNodeData(obj)

        items = {}
        for child in obj.Group:
            child.Proxy.backupNodeData(child)
            items[child.Label] = json.loads(child.NodeDataString)

        self.nodeData["Entities"]["items"] = copy.deepcopy(items)
        # then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def SnappyGeDialogClosed(self, obj, geometryLabel):
        '''
            create a new snappy geometry entity node
            update the data from dialog to FreeCAD object
            also update the BC nodes with the new geometry
        '''

        # call when created new GE node
        num = len(obj.Group)

        # take the entity node data and update its title with the geometry name
        entityNodeData = copy.deepcopy(self.nodeData["Entities"]["TemplateEntity"])
        entityNodeData["WebGui"]["Schema"]["title"] = "SnappyHexMesh " + geometryLabel

        # create the FC obj
        GeoEntity_obj = HermesNode.makeNode("snappy_"+geometryLabel, obj, str(num), entityNodeData)

        # check object has been created
        if GeoEntity_obj is None:
            return None

        # geometryObj = FreeCAD.ActiveDocument.getObject(geometryName)
        geometryObj = FreeCAD.ActiveDocument.getObjectsByLabel(geometryLabel)[0]
        if geometryObj is not None:
            GeoEntity_obj.partLinkName = geometryObj.Name
            GeoEntity_obj.Proxy.doubleClickedNode(GeoEntity_obj)
        else:
            FreeCAD.Console.PrintMessage("SnappyGeDialogClosed: geometryObj is None \n")

        bcObj = FreeCAD.ActiveDocument.getObject("BoundaryCondition")
        if bcObj is not None:
            bcObj.Proxy.updateBCPartList(bcObj)
            bcObj.touch()

        return

    def jsonToJinja(self, obj):
        ''' convert the json data to "inputParameters" structure '''
        objects = {}
        for child in obj.Group:
            objects[child.partLinkName] = child.Proxy.jsonToJinja(child)

        return dict(objects=objects)

# =============================================================================
# #_SnappyHexMeshGeometryEntity
# =============================================================================
class _SnappyHexMeshGeometryEntity(_WebGuiNode):

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)


    def jsonToJinja(self, obj):
        ''' convert the json data to "inputParameters" structure '''

        jinjaObj = dict()
        for key,val in self.nodeData["WebGui"]["formData"].items():
            updateKey = key.replace("TSM", "")
            jinjaObj[updateKey] = val

        # turn refinementRegions levels from string to arrays
        # for mode distance - list of string to list of arrays
        if "refinementRegions" in jinjaObj.keys():
            if "mode" not in jinjaObj["refinementRegions"]:
                    pass
            elif jinjaObj["refinementRegions"]["mode"] == "distance":
                levels = list()
                for level in jinjaObj["refinementRegions"]["levels"]:
                    levels.append(self.stringToArray(level))
                jinjaObj["refinementRegions"]["levels"] = levels
            else:
                # for mode inside/outside just to strung to arr
                jinjaObj["refinementRegions"]["levels"] = self.stringToArray(jinjaObj["refinementRegions"]["levels"])

            # turn refinementSurfaceLevels from string to arrays
            if "refinementSurfaceLevels" in jinjaObj.keys():
                jinjaObj["refinementSurfaceLevels"] = self.stringToArray(jinjaObj["refinementSurfaceLevels"])

        # mv the regions from array to dict structure
        if "regions" in jinjaObj.keys():
            new_regions = dict()
            for reg in jinjaObj["regions"]:
                new_regions[reg["regionName"]] = dict(name=reg["regionName"], type=reg["regionType"])
            jinjaObj["regions"] = new_regions


        return jinjaObj

    def stringToArray(self, stringObj):
        ''' convert from string to array of numbers '''
        if type(stringObj) is not str:
            FreeCAD.Console.PrintMessage("stringObj is not string. stringObj = "+ str(stringObj) + "and its type is " + str(type(stringObj)) + "\n")
            return

        l_stringObj = stringObj.split(",") if "," in stringObj else stringObj.split(" ")
        arr = list()
        for item in l_stringObj:
            if "(" in item:
                tmp = item.replace("(", "")
                if len(tmp) > 0:
                    arr.append(float(tmp))
            elif ")" in item:
                tmp = item.replace(")", "")
                if len(tmp) > 0:
                    arr.append(float(tmp))
            elif ")" in item:
                tmp = item.replace(",", "")
                if len(tmp) > 0:
                    arr.append(float(tmp))
            else:
                arr.append(float(item))
        return arr


# =============================================================================
# SnappyHexMeshGeometryEntityDialogPanel
# =============================================================================
# Path To GE UI
snappy_ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
path_to_snappyGe_ui = snappy_ResourceDir + "Mod/Hermes/Resources/ui/snappygeometry.ui"

class SnappyHexMeshGeometryEntityDialogPanel:

    def __init__(self, obj):
        # Create widget from ui file
        self.form = FreeCADGui.PySideUic.loadUi(path_to_snappyGe_ui)

    def addGemotry(self, gemetry):
        # add  geType to options at GE dialog
        self.form.m_pGeometryCB.addItem(gemetry)

    def setCurrentGeometry(self,GemetryName):
        # update the current value in the comboBox
        self.form.m_pGeometryCB.setCurrentText(GemetryName)

    def setCallingObject(self, callingObjName):
        # get obj Name, so in def 'accept' can call the obj
        self.callingObjName = callingObjName

    def accept(self):
        # Happen when Close Dialog
        # get the current GE type name from Dialog
        Geometry = self.form.m_pGeometryCB.currentText()

        # calling the nodeObj from name
        callingObject = FreeCAD.ActiveDocument.getObject(self.callingObjName)

        # calling the function that create the new GE Object
        callingObject.Proxy.SnappyGeDialogClosed(callingObject, Geometry)

        # close the Dialog in FreeCAD
        FreeCADGui.Control.closeDialog()

    def reject(self):
        # check if it reset choices
        return True

# =============================================================================
# #_CommandSnappyHexMeshPointSelection
# =============================================================================
from DraftTools import Point
from DraftGui import todo

class _CommandSnappyHexMeshPointSelection(Point):
    """ Geometry Definer point selection command definition """

    def GetResources(self):
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
        icon_path = ResourceDir + "Mod/Hermes/Resources/icons/blue_ball.png"
        # icon_path = os.path.join(CfdTools.get_module_path(), "Gui", "Resources", "icons", "physics.png")

        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("SnappyHexMeshPoint", "3D point snappyHexMesh"),
                'Accel': "",
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("SnappyHexMeshPoint", "Create a 3D point for snappyHexMesh")}

    def IsActive(self):
        snappy = FreeCAD.ActiveDocument.getObjectsByLabel("SnappyHexMesh")[0]
        if snappy is not None:
            # check if point already exist
            docObjs = [obj.Label for obj in FreeCAD.ActiveDocument.Objects if "locationInMesh" in obj.Label]
            if len(docObjs) > 0:
                return False

            return True

        return False

    # def Activated(self):
    #
    #     super().Activated()

    def click(self, event_cb=None):
        super().click()
        FreeCAD.ActiveDocument.recompute()

        # todo.delayAfter(self.linkToSnappy, [])
        todo.delayAfter(self.linkToSnappy, None)
        # QtCore.QTimer.singleShot(0, self.linkToSnappy)

    def linkToSnappy(self):


        # snappyObj = FreeCAD.ActiveDocument.getObjectsByLabel("SnappyHexMesh")[0]
        castellObj = FreeCAD.ActiveDocument.getObjectsByLabel("castellatedMeshControls")[0]
        if castellObj is None:
            return
        # FreeCADGui.doCommand("FreeCAD.Console.PrintMessage('Objects = ' + str([obj.Label for obj in FreeCAD.ActiveDocument.Objects]) + '\n')")
        # FreeCAD.Console.PrintMessage("Objects = " + str([obj.Label for obj in FreeCAD.ActiveDocument.Objects]) + "\n")

        snappyPoint = FreeCAD.ActiveDocument.Objects[-1]
        if "Point" not in snappyPoint.Label:
            return
        # snappyPoint = Draft.makePoint(0, 0, 0, point_size=10)
        snappyPoint.Label = "Point_locationInMesh"


        castellObj.locationInMesh = snappyPoint


# if FreeCAD.GuiUp:
#     FreeCADGui.addCommand('SnappyHexMeshPointSelection', _CommandSnappyHexMeshPointSelection())

# =============================================================================
# #_CommandSnappyHexMeshObjSelection
# =============================================================================
class _CommandSnappyHexMeshObjSelection:
    """ Geometry Definer selection command definition """

    def GetResources(self):
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
        icon_path = ResourceDir + "Mod/Hermes/Resources/icons/GeometryDefiner.png"
        # icon_path = os.path.join(CfdTools.get_module_path(), "Gui", "Resources", "icons", "physics.png")

        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("SnappyHexMeshObjSelection", "Export SnappyHexMesh obj"),
                'Accel': "",
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("SnappyHexMeshObjSelection", "Export SnappyHexMesh Geometries as obj")}

    def IsActive(self):
        snappy = FreeCAD.ActiveDocument.getObjectsByLabel("SnappyHexMesh")[0]
        if snappy is not None:
            snappyGeo = [obj for obj in snappy.Group if obj.Name == "Geometry"]
            if len(snappyGeo[0].Group) > 0:
                return True
            else:
                return False
        return False

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Choose export")

        # get SnappyHexMesh FreeCAD object
        snappy = FreeCAD.ActiveDocument.getObjectsByLabel("SnappyHexMesh")[0]
        if snappy is None:
            return

        # get the snappy Geometry node
        snappyGeo = [obj for obj in snappy.Group if obj.Name == "Geometry"]

        # create list from all Geometry objects linked to the snappyGeometries obj s
        objs = []
        for child in snappyGeo[0].Group:
            part = FreeCAD.ActiveDocument.getObject(child.partLinkName)
            objs.append(part)

        # save file in wanted location
        self.save_mult_objs_file(objs)
        # self.save_one_obj_file(objs)

        del objs

    def save_mult_objs_file(self, objs):
        ''' save multiply snappy geometries as .obj files, in a wanted location'''
        import Mesh

        # what the dialog open dir - path
        # path = FreeCAD.ConfigGet("UserAppData")
        path = os.getcwd()

        try:
            SaveName = QFileDialog.getExistingDirectory(None, "Open Directory", path)  # PyQt4
        #                          "here the text displayed on windows" "here the filter (extension)"

        except Exception:
            SaveName = QFileDialog.getExistingDirectory(None, "Open Directory", path)  # PyQt4

        #       "here the text displayed on windows" "here the filter (extension)"

        if SaveName == "":  # if the name file are not selected then Abord process
            FreeCAD.Console.PrintMessage("Export obj file aborted" + "\n")
        else:  # if the name file are selected

            # loop all objs, and export file to each one
            for obj in objs:
                SaveName = path + "/" + obj.Label

                FreeCAD.Console.PrintMessage(
                    "Exporting file " + SaveName + ".obj" + "\n")  # text displayed to Report view (Menu > View > Report view checked)
                try:  # if error detected to export ...
                    outpath = u"" + SaveName + ".obj"
                    Mesh.export([obj], outpath)
                    # must export list of object - typewise
                except Exception:  # if error detected to write
                    FreeCAD.Console.PrintError(
                            "Error Exporting file " + "\n")  # detect error ... display the text in red (PrintError)

    def save_one_obj_file(self, objs):
        ''' save 1 .obj file in wanted location'''
        import Mesh
        import re

        # what the dialog open dir - path
        # path = FreeCAD.ConfigGet("UserAppData")
        path = os.getcwd()

        try:
            SaveName = QFileDialog.getSaveFileName(None, QString.fromLocal8Bit("Save Geometry Definer as obj file"), path,
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



