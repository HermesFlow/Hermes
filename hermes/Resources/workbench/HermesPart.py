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

        maxmin={'min': 1e6 , 'max': -1e6}
        self.extrema = {'x': maxmin, 'y': maxmin, 'z': maxmin}

    def getFreeCADpart(self):
        return self.doc.getObjectsByLabel(self.partName)[0]

    def getpartDict(self):

        part = {}
        vertices = {}

        # call fuctions that locate all vertices and faces
        vertices["FreeCAD"] = self.getVertices()
        vertices["openFoam"] = self.sortVertices()
        faces = self.getFaces(vertices["openFoam"])


        # save the data into a part dict
        part = {"Vertices": vertices, "Faces": faces}

        return part

    def getFaces(self, partVertices):

        # get the Faces from the part
        listOfShapeFaces = self.partObj.Shape.Faces

        partFaces = {}

        # loop all faces of the part
        for i in range(len(listOfShapeFaces)):


            # define face name and it to the dict
            face_name = "Face" + str(i+1)
            partFaces[face_name]={}

            # get the Vertices of the Face
            listOfFaceVertices = self.partObj.Shape.Faces[i].Vertexes
            vertexList = []
            # loop all Vertices of the face and connect to the partVertices dict name
            for j in range(len(listOfFaceVertices)):
                verName = self.attachVerticesToFace(listOfFaceVertices[j], partVertices)
                vertexList.append(verName)

            # sort the face vertices clockwise when looking from the center of the cube
            sortList = self.sortFaceVertecesClockwise(partVertices, vertexList)

            # add the sorted list of vertices name to the Face dict
            partFaces[face_name]["vertices"] = sortList

        return partFaces

    def sortFaceVertecesClockwise(self, partVertices, vertexList):

        # get the plane of the face (constant x/y/z : min/max)
        plane = self.getPlane(partVertices, vertexList)

        # 2 cases to arrange vertices clockeise from center point of view
        if (plane == ['x', 'min']) or (plane == ['y', 'max']) or (plane == ['z', 'min']):
            case = True
        else:
            case = False

        # get the sort list
        sortList = self.CreateVertexList(partVertices, vertexList, plane, case)

        return sortList

    def CreateVertexList(self, partVertices, vertexList, plane, case):

        sortList = []

        # create vertices and add to the sorted list
        for i in range(len(vertexList)):
            # create a new vertex
            ver = {}

            # plane = [ coordinate x/y/z , max/min] -> example: ['x','min']
            # set vertex const value of the plane
            ver[plane[0]] = self.extrema[plane[0]][plane[1]]

            # for the rest of coordinates - define the values as follow
            #         [ vertex 0,  vertex 1,  vertex 2,  vertex 3]
            # case 1: [(min,min), (min,max), (max,max), (max,min)]
            # case 2: [(min,min), (max,min), (max,max), (min,max)]
            if i == 0:
                for o in self.extrema:
                    if o != plane[0]:
                        ver[o] = self.extrema[o]['min']
            elif i == 1:
                ver = self.sortMinMax(ver, plane) if case else self.sortMaxMin(ver, plane)
            elif i == 2:
                for o in self.extrema:
                    if o != plane[0]:
                        ver[o] = self.extrema[o]['max']
            elif i == 3:
                ver = self.sortMaxMin(ver, plane) if case else self.sortMinMax(ver, plane)

            # get the vertex name from the partVertices
            verName = self.attachVerticesToVertexList(ver, partVertices)

            # make sure the vertex is on the face
            if verName in vertexList:
                # add the vertex to the sorted list
                sortList.append(verName)
            else:
                print("===Error in attach vertices to face =====\n")

        return sortList

    def sortMinMax(self, ver, plane):
        '''
        asuuming order [x,y,z] - define the vars that not constant on the
        plane to first min and then max - depend on that order.
        plane: example - ['x','min']
        '''
        count = 0
        for o in self.extrema:
            if (o != plane[0]):
                ver[o] = self.extrema[o]['min'] if count == 0 else self.extrema[o]['max']
                count += 1
        return ver

    def sortMaxMin(self, ver, plane):
        '''
        asuuming order [x,y,z] - define the vars that not constant on the
        plane to first max and then min - depend on that order.
        plane: example - ['x','min']
        '''
        count = 0
        for o in self.extrema:
            if (o != plane[0]):
                ver[o] = self.extrema[o]['max'] if count == 0 else self.extrema[o]['min']
                count += 1
        return ver

    def getPlane(self, partVertices, vertexList):

        # define a sum var in each direction
        sum = {'x': 0, 'y': 0, 'z': 0}

        # sum all coordinates values in each direction
        for i in range(len(vertexList)):
            verName = vertexList[i]
            sum['x'] += partVertices[verName]["coordinates"]['x']
            sum['y'] += partVertices[verName]["coordinates"]['y']
            sum['z'] += partVertices[verName]["coordinates"]['z']

        # loop sum
        for cor in sum:
            # if the sum in the direction is zero - plane on constant cor min
            if (sum[cor]) == 0:
                return [cor, 'min']
            # if the sum in the direction is 4*max - plane on constant cor max
            elif sum[cor] == 4 * self.extrema[cor]['max']:
                return [cor, 'max']

    def getVertices(self):

        partVertices = {}
        # get the Vertices from the part
        listOfShapeVertices = self.partObj.Shape.Vertexes

        # define general coordinates dict
        pos = {'x': None, 'y': None, 'z': None }

        # loop all vertices and save them and its coordinates
        for i in range(len(listOfShapeVertices)):
            # set vertex name and add it the vertices dict
            name = str(i)
            partVertices[name] = {}

            # get the current vertex coorsinates
            pos['x'] = listOfShapeVertices[i].X
            pos['y'] = listOfShapeVertices[i].Y
            pos['z'] = listOfShapeVertices[i].Z

            # get max/min values for x,y,z
            for oKey, oVal in self.extrema.items():
                if oVal['min'] > pos[oKey]:
                    self.extrema[oKey]['min'] = pos[oKey]
                if oVal['max'] < pos[oKey]:
                    self.extrema[oKey]['max'] = pos[oKey]

                        # add the coordinates to the current vertex
            partVertices[name]["coordinates"] = pos.copy()

        return partVertices

    def sortVertices(self):
        newOrder = {}
        index = 0
        for k, kv in self.extrema['z'].items():
            for j, jv in self.extrema['y'].items():
                # for i in self.extrema['x']:
                if (index == 0) or (index == 4):
                    newOrder[str(index)] = {'coordinates': {'x': self.extrema['x']['min'], 'y': jv, 'z': kv }}
                    newOrder[str(index+1)] = {'coordinates': {'x': self.extrema['x']['max'], 'y': jv, 'z': kv }}
                else:
                    newOrder[str(index)] = {'coordinates': {'x': self.extrema['x']['max'], 'y': jv, 'z': kv}}
                    newOrder[str(index + 1)] = {'coordinates': {'x': self.extrema['x']['min'], 'y': jv, 'z': kv}}
                index += 2
        # print(newOrder)
        return newOrder


    def attachVerticesToFace(self, vertex, partVertices):

        # get the current vertex coordinates(from FC object)
        x = vertex.X
        y = vertex.Y
        z = vertex.Z

        # compare the coordinates of the vertex and the partVertices items
        # in case all coordinates fit, return the vertex name
        for itemKey, itemVal in partVertices.items():
            # print(itemKey + ":" + itemVal)
            if (itemVal['coordinates']['x'] == x) and (itemVal['coordinates']['y'] == y) and (itemVal['coordinates']['z'] == z):
                return itemKey

        return None

    def attachVerticesToVertexList(self, vertex, partVertices):

        # get the current vertex coordinates(from dict)
        x = vertex['x']
        y = vertex['y']
        z = vertex['z']

        # compare the coordinates of the vertex and the partVertices items
        # in case all coordinates fit, return the vertex name
        for itemKey, itemVal in partVertices.items():
            # print(itemKey + ":" + itemVal)
            if (itemVal['coordinates']['x'] == x) and (itemVal['coordinates']['y'] == y) and (itemVal['coordinates']['z'] == z):
                return itemKey

        return None

