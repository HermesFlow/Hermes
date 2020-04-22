import jinja2

class C_transform(object,):
    '''
        will transform controlDict from JSON structure
        to openFOAM structure using jinja  '''

    # define the template of controlDict
    _basicControlDictTemplate = """
/*--------------------------------*- C++ -*----------------------------------*\ 
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  3.0.1                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/

FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

application     {{input.application}};

startFrom       {{input.startFrom}};

startTime       {{input.startTime}};

stopAt          {{input.stopAt}};

endTime         {{input.endTime}};

deltaT          {{input.deltaT}};

writeControl    {{input.writeControl}};

writeInterval   {{input.writeInterval}};

purgeWrite      {{input.purgeWrite}};

writeFormat     {{input.writeFormat}};

writePrecision  {{input.writePrecision}};

writeCompression {{input.writeCompression}};

timeFormat      {{input.timeFormat}};

timePrecision   {{input.timePrecision}};

runTimeModifiable {{input.runTimeModifiable}};

// adjustTimeStep  yes;

// maxCo           1;

interpolate     {{input.interpolate}};

functions       {{input.functions}};
        
"""

    def __init__(self):
        pass


    def transform(self, input):
        # get the dict input values of controlDict and push it to the template with jinja render
        rtemplate = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(self._basicControlDictTemplate)
        return rtemplate.render(input=input)
