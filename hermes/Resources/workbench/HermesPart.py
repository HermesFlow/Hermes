# FreeCAD Part module
# (c) 2001 Juergen Riegel
#
# Part design module

# ***************************************************************************
# *   (c) Juergen Riegel (juergen.riegel@web.de) 2002                       *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# *   Juergen Riegel 2002                                                   *
# ***************************************************************************/

import FreeCAD

class HermesPart:
    '''
    The HermesPart class will translate the FreeCAD part objects data,
    into dictionary structure that will allow an eazy way to transfer data
    into JSON
    '''

    def __init__(self, Name):
        self.partName = Name
        self.doc = FreeCAD.ActiveDocument
        self.partObj = self.getFreeCADpart()
        self.partVertices = {}
        self.partFaces = {}

    def getFreeCADpart(self):
        return self.doc.getObjectsByLabel(self.partName)[0]

    def getpartDict(self):

        # call fuctions that locate all vertices and faces
        self.getVertices()
        self.getFaces()

        # save the data into a part dict
        part = {"Vertices": self.partVertices, "Faces": self.partFaces}

        return part

    def getFaces(self):

        # get the Faces from the part
        listOfShapeFaces = self.partObj.Shape.Faces

        # loop all faces of the part
        for i in range(len(listOfShapeFaces)):

            # define face name and it to the dict
            face_name = "Face" + str(i + 1)
            self.partFaces[face_name]={}

            # get the Vertices of the Face
            listOfFaceVertices = self.partObj.Shape.Faces[i].Vertexes
            vertexList = []

            # loop all Vertices of the face and connect to the self.partVertices dict name
            for j in range(len(listOfFaceVertices)):
                verName = self.attachVerticesToFace(listOfFaceVertices[j])
                vertexList.append(verName)

            # add the list of vertices name to the Face dict
            self.partFaces[face_name]["vertices"] = vertexList
            # print(str(face_name) + ":" + str(self.partFaces[face_name]) + "\n")


    def getVertices(self):

        # get the Vertices from the part
        listOfShapeVertices = self.partObj.Shape.Vertexes

        # define general coordinates dict
        coordinates = {'x': None, 'y': None, 'z': None }

        # loop all vertices and save them and its coordinates
        for i in range(len(listOfShapeVertices)):
            # set vertex name and add it the vertices dict
            name = str(i + 1)
            self.partVertices[name] = {}

            # get the current vertex coorsinates
            coordinates['x'] = listOfShapeVertices[i].X
            coordinates['y'] = listOfShapeVertices[i].Y
            coordinates['z'] = listOfShapeVertices[i].Z

            # add the coordinates to the current vertex
            self.partVertices[name]["coordinates"] = coordinates.copy()

    def attachVerticesToFace(self, vertex):

        # get the current vertex coordinates
        x = vertex.X
        y = vertex.Y
        z = vertex.Z

        # compare the coordinates of the vertex and the self.partVertices items
        # in case all coordinates fit, return the vertex name
        for itemKey,itemVal in self.partVertices.items():
            if (itemVal['coordinates']['x'] == x) and (itemVal['coordinates']['y'] == y) and (itemVal['coordinates']['z'] == z):
                return itemKey

        return None
