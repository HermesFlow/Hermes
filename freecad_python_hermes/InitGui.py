# HermesFlow gui init module  
# 
#

#***************************************************************************
#*   Based on (c) Juergen Riegel (juergen.riegel@web.de) 2002                       *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#*   Juergen Riegel 2002                                                   *
#***************************************************************************/

import FreeCAD,FreeCADGui, WebGui


class Hermes ( Workbench ):
    "Web workbench object"
    def __init__(self):
        self.__class__.Icon = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/hermes.png"
        self.__class__.MenuText = "Hermes"
        self.__class__.ToolTip = "Hermes"

    def Initialize(self):
        # load the module
        import HermesGui

        list = ["CreateWorkflow"]
        self.appendToolbar("HermesToolbar", list)


#    def GetClassName(self):
#        return "Hermes::Workbench"

Gui.addWorkbench(Hermes())



