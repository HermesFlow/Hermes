# import FreeCAD modules
import FreeCAD, FreeCADGui, WebGui
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

    import PySide
    # from PySide import QtGui, QtCore
    # from PySide.QtGui import *
    # from PySide.QtCore import *


# python modules
from PyQt5 import QtGui,QtCore
import json
import pydoc
import os
import sys
import copy

# Hermes modules
import HermesTools
from HermesTools import addObjectProperty
import HermesGeometryDefinerNode
import HermesPart
import Draft
from HermesBlockMesh import HermesBlockMesh

# from hermes.Resources.workbench import _WebGuiNode
# import _WebGuiNode
# sys.path.append(".")
# from hermes.Resources.workbench.HermesNode import _WebGuiNode
from HermesNode import _WebGuiNode, _HermesNode
import HermesNode


# =============================================================================
# #_SnappyHexMesh
# =============================================================================
class _SnappyHexMesh(_WebGuiNode):
    #    super().funcName(var1,var,2..) - allow to use the function of the Parent,
    #    and add current class functionalites

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

        geometry_obj = HermesNode.makeNode("Geometry", obj, str(0), self.nodeData["Geometry"])
        refinement_obj = HermesNode.makeNode("Refinement", obj, str(0), self.nodeData["Refinement"])


        # create Geometry obj
            # this also a webGuiNode

        # create refinement object
        # this node is just show without any action (read only for now?)

    def doubleClickedNode(self, obj):
        # super().doubleClickedNode(obj)
        self.updateJson(obj)
        self.selectNode(obj)
        obj.IsActiveObj = True


    def selectNode(self, obj):
        # check point exist
        snappyPoint = [obj for obj in FreeCAD.ActiveDocument.Objects if "locationInMesh" in obj.Label]
        if len(snappyPoint) > 0:
            snappyPoint = snappyPoint[0]
            x = format(float(snappyPoint.X), '.2f')
            y = format(float(snappyPoint.Y), '.2f')
            z = format(float(snappyPoint.Z), '.2f')

            locationString = "(" + x + " " + y + " " + z + ")"

            self.nodeData["WebGui"]["formData"]["castellatedMeshControls"]["locationInMesh"] = locationString
        # update Point coordinate

        #continue as webgui
        super().selectNode(obj)

        #
        # self.updatePointFromWebgui()


    def backupNodeData(self, obj):
        # backup the data of the last node pressed
        super().backupNodeData(obj)

        for child in obj.Group:
            child.Proxy.backupNodeData(child)
            self.nodeData[child.Name] = json.loads(child.NodeDataString)

        self.updatePointFromWebgui()

        # then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def updateJson(self, obj):
        obj.NodeDataString = json.dumps(self.nodeData)




    def updatePointFromWebgui(self):
        snappyPoint = [obj for obj in FreeCAD.ActiveDocument.Objects if "locationInMesh" in obj.Label]
        if len(snappyPoint) > 0:
            snappyPoint = snappyPoint[0]
        else:
            return

        locationString = self.nodeData["WebGui"]["formData"]["castellatedMeshControls"]["locationInMesh"]
        l_location = locationString.split(" ")
        coordinates = list()
        for item in l_location:
            if "(" in item:
                coordinates.append(item.replace("(", ""))
            elif ")" in item:
                coordinates.append(item.replace(")", ""))
            else:
                coordinates.append(item)

        # FreeCAD.Console.PrintMessage("l_location = " + str(l_location) + "\n")
        # FreeCAD.Console.PrintMessage("coordinates = " + str(coordinates) + "\n")

        if len(coordinates) == 3:
            # snappyPoint = snappyPoint[0]
            snappyPoint.X = coordinates[0]
            snappyPoint.Y = coordinates[1]
            snappyPoint.Z = coordinates[2]

# =============================================================================
# #_SnappyHexMeshRefinement
# =============================================================================
class _SnappyHexMeshRefinement(_WebGuiNode):
    #    super().funcName(var1,var,2..) - allow to use the function of the Parent,
    #    and add current class functionalites

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

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
    #    super().funcName(var1,var,2..) - allow to use the function of the Parent,
    #    and add current class functionalites

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def initializeFromJson(self, obj):
        super().initializeFromJson(obj)

        for itemKey, itemVal in self.nodeData["Entities"]["items"].items():
            l = len(obj.Group)
            GeoEntity_obj = HermesNode.makeNode(itemKey, obj, str(l), itemVal)



    def doubleClickedNode(self, obj):
        super().doubleClickedNode(obj)
        # self.selectNode(obj)
        # num = len(obj.Group)
        # GeoEntity_obj = makeNode("GeoEntity_"+str(num), obj, str(num), copy.deepcopy(self.nodeData["Entities"]["TemplateEntity"]))

        # -------- panel dialog box  definitions --------------

        # create snappyGeDialog Object
        snappyGeDialog = SnappyHexMeshGeometryEntityDialogPanel(obj)

        # get Parts from FC
        Parts = [FCobj.Label for FCobj in FreeCAD.ActiveDocument.Objects if FCobj.Module == 'Part']

        # make sure part won't be chosen twice
        for child in obj.Group:
            if child.partLink.Label in Parts:
                Parts.remove(child.partLink.Label)

        # try without Facebinder (BlockMesh entities) - any link of part give him a parent
        # it is ok for BlockMesh but what if there will be other links later?
        # Parts = []
        # for FCobj in FreeCAD.ActiveDocument.Objects:
        #     if FCobj.Module == 'Part':
        #         if FCobj.getParentGroup() is None:
        #             Parts.append(FCobj.Name)
        #         elif FCobj.getParentGroup().Module != 'App':
        #             Parts.append(FCobj.Name)

        # FreeCAD.Console.PrintMessage("Parts = " + str(Parts) + "\n")

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
        # backup the data of the last node pressed
        super().backupNodeData(obj)

        items = {}
        for child in obj.Group:
            child.Proxy.backupNodeData(child)
            items[child.Name] = json.loads(child.NodeDataString)

        self.nodeData["Entities"]["items"] = copy.deepcopy(items)
        # then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def SnappyGeDialogClosed(self, obj, geometryLabel):
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
            GeoEntity_obj.partLink = geometryObj
            GeoEntity_obj.Proxy.doubleClickedNode(GeoEntity_obj)
        else:
            FreeCAD.Console.PrintMessage("SnappyGeDialogClosed: geometryObj is None \n")



        return

# =============================================================================
# #_SnappyHexMeshGeometryEntity
# =============================================================================
class _SnappyHexMeshGeometryEntity(_WebGuiNode):
    #    super().funcName(var1,var,2..) - allow to use the function of the Parent,
    #    and add current class functionalites

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)
        # FreeCAD.Console.PrintMessage("__init__: GeometryEntity nodadata = " + str(self.nodeData))



    # def doubleClickedNode(self, obj):
    #     # super().doubleClickedNode(obj)
    #     self.selectNode(obj)
    #     self.backupNodeData(obj)
    #     # FreeCAD.Console.PrintMessage("GeometryEntity nodadata = " + str(self.nodeData))

    # def backupNodeData(self, obj):
    #     # backup the data of the last node pressed
    #     super().backupNodeData(obj)
        # FreeCAD.Console.PrintMessage("===============================================================\n")
        # FreeCAD.Console.PrintMessage("Node: Name = " + obj.Name + "; Label = " + obj.Label +"\n")
        # FreeCAD.Console.PrintMessage("self.nodeData[WebGui] = " + str(self.nodeData["WebGui"]) + "\n")

    #
    #     # then Update nodeData  at the NodeDataString by converting from json to string
    #     obj.NodeDataString = json.dumps(self.nodeData)

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
    """ Geometry Definer selection command definition """

    def GetResources(self):
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
        icon_path = ResourceDir + "Mod/Hermes/Resources/icons/point01.png"
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

        todo.delayAfter(self.linkToSnappy,[])

    def linkToSnappy(self):


        snappyObj = FreeCAD.ActiveDocument.getObjectsByLabel("SnappyHexMesh")[0]
        # FreeCADGui.doCommand("FreeCAD.Console.PrintMessage('Objects = ' + str([obj.Label for obj in FreeCAD.ActiveDocument.Objects]) + '\n')")
        # FreeCAD.Console.PrintMessage("Objects = " + str([obj.Label for obj in FreeCAD.ActiveDocument.Objects]) + "\n")


        snappyPoint = FreeCAD.ActiveDocument.Objects[-1]
        if "Point" not in snappyPoint.Label:
            return
        # snappyPoint = Draft.makePoint(0, 0, 0, point_size=10)
        snappyPoint.Label = "Point_locationInMesh"

        snappyObj.locationInMesh = snappyPoint

        # nodeData = json.loads(snappyObj.NodeDataString)
        nodeData = snappyObj.Proxy.nodeData

        x = format(float(snappyPoint[0].X), '.2f')
        y = format(float(snappyPoint[0].Y), '.2f')
        z = format(float(snappyPoint[0].Z), '.2f')

        locationString = "(" + x + " " + y + " " + z + ")"

        nodeData["WebGui"]["formData"]["castellatedMeshControls"]["locationInMesh"] = locationString

        # snappyObj.NodeDataString = json.dumps(nodeData)
        snappyObj.Proxy.nodeData = nodeData
        snappyObj.Proxy.backupNodeData(snappyObj)

if FreeCAD.GuiUp:
    FreeCADGui.addCommand('SnappyHexMeshPointSelection', _CommandSnappyHexMeshPointSelection())

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
                'MenuText': QtCore.QT_TRANSLATE_NOOP("SnappyHexMeshObjSelection", "SnappyHexMesh obj"),
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
            objs.append(child.partLink)

        # save file in wanted location
        self.save_mult_objs_file(objs)

        del objs

    def save_mult_objs_file(self, objs):
        import Mesh

        #get working directory
        path = os.getcwd()


        # loop all objects and export an .obj file to each one
        for obj in objs:
            SaveName = path + "/" + obj.Label

            FreeCAD.Console.PrintMessage(
                "Exporting file " + SaveName + ".obj" + "\n")

            try:  # if error detected to export ...
                outpath = u"" + SaveName + ".obj"
                Mesh.export([obj], outpath)
            except Exception:  # if error detected to write
                FreeCAD.Console.PrintError(
                        "Error Exporting file " + "\n")  # detect error ... display the text in red (PrintError)

    def save_one_obj_file(self, objs):
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




if FreeCAD.GuiUp:
    FreeCADGui.addCommand('SnappyHexMeshObjSelection', _CommandSnappyHexMeshObjSelection())