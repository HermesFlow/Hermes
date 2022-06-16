
import FreeCAD,FreeCADGui, WebGui
# from hermes.Resources.workbench.openFOAM2.mesh import HermesSnappyHexMesh


class Hermes ( Workbench ):
    "Web workbench object"
    def __init__(self):
        self.__class__.Icon = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/hermes.png"
        self.__class__.MenuText = "Hermes"
        self.__class__.ToolTip = "Hermes"

    def Initialize(self):
        # load the module
        import HermesGui

        # ---------- define snappyHexMesh command -----------
        list = ["CreateWorkflow"]

        import importlib
        import os

        # define paths
        workbencj_path = "hermes.Resources.workbench"
        paths = ["openFOAM2.mesh.HermesSnappyHexMesh._CommandSnappyHexMeshPointSelection",
                 "openFOAM2.mesh.HermesSnappyHexMesh._CommandSnappyHexMeshObjSelection"]

        for path in paths:
            # build path - join and make sure path with '.'
            path = os.path.join(workbencj_path, path)
            path = path.replace("/", ".")
            module_name, class_name = path.rsplit(".", 1)
            try:
                # get class and define command, and it to list of commands
                command_class = getattr(importlib.import_module(module_name), class_name)
                command_name = class_name.replace("_Command", "")
                # FreeCAD.Console.PrintMessage("command_name = " + command_name + "\n")
                FreeCADGui.addCommand(command_name, command_class())
                list.append(command_name)

            except Exception:  # if error detected to write
                FreeCAD.Console.PrintError("Error locating class" + class_name + "\n")

        # -------------------------------------

        self.appendToolbar("HermesToolbar", list)
        self.appendMenu("Hermes", list)

#    def GetClassName(self):
#        return "Hermes::Workbench"

Gui.addWorkbench(Hermes())



