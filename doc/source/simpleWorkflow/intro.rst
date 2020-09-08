
Simple Workflow
================

Workflow Steps
###############

A simple workflow will include the steps to create all the needed files for an openFOAM run, using the FreeCAD and its Hermes module.

    1.  Open FreeCAD and create a new document. 
    2.  Choose the Hermes module, and create a new HermesWorkflow object by pressing its symbol
    3.  Import the basic JSON file of the workflow
		-   Press the HermesWorkflow object, a properties panel will appear below.
		-   In the IO section choose the "Import JsonFile" value, click on the 3 point button and choose the wanted file.
		-	All the nodes that have been defined in the JSON file should be load automatically under the HermesWorkflow object

    4.	Update the data in each node, if needed
		-	one click on the node - will show the properties panel of the node
		-	 double click on the node :
		-	WebGui node - will display the browser of the node
		-	BC, Boundry condition node - will allow you to add a new boundary condition to the case.
		-	Other nodes, for now, have no functionality.

    5.	Export an updated JSON File 
		
        there are two options to export the updated JSON file-

            A.	Whole workflow:

                -	click the HermesWorkflow object, a properties panel will appear below.
                - 	In the IO section choose the "Export JsonFile" value, click on the 3 point button and choose the wanted directory the file will be export to.
                -   the JSON file will be export to the directory with the name of the HermesWorkflow name. In addition, the root value at the JSON will be "null" 

            B.	Specific node:

                -   click any node, a properties panel will appear below.
                -   In the IO section choose the "Export JsonFile" value, click on the 3 point button and choose the wanted directory the file will be export to.
                -   the JSON file will be export to the directory with the name of the node name. In addition, the root value at the JSON will also be the node name

The nodes for an openFOAM
##########################

In the simple workflow, there are different types of nodes-

    1.  WebGui nodes
    2.  Boundry Condition nodes
    3.  System operation nodes


WebGui nodes
--------------

The nodes included:

    -   snappyHexMesh
    -   controlDict
    -   fvSchemes
    -   fvSolution
    -   transportProperties
    -   turbulence

At each node from the list, there are parameters that need to be defined to use the openFOAM method.
Those parameters will be displayed in a specific browser of the chosen node. 
After Updating the value of each wanted parameter, the data will be saved into the JSON structure.
The last step will create an openFOAM dictionary from the data been saved at the JSON structure, in the name of the node.


Boundry Condition nodes
------------------------




System operation nodes
-----------------------

The nodes included:

    -   copyDirectory
    -   RunPythonScript
    -   RunOsCommand












 
