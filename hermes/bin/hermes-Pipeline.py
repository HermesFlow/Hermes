import argparse
from hermes import expandPipeline
import json

parser = argparse.ArgumentParser()
parser.add_argument('command', nargs=1, type=str)
parser.add_argument('args', nargs='*', type=str)

args = parser.parse_args()

exapnder = expandPipeline()

def expand_handler(arguments):

    templatePath = arguments[0]
    newTemplatePath = arguments[1]
    parametersPath = arguments[2] if len(arguments) > 2 else None

    newTemplate = exapnder.expand(pipelinePath=templatePath,parametersPath=parametersPath)
    with open(newTemplatePath, 'w') as fp:
        json.dump(newTemplate, fp)

globals()['%s_handler' % args.command[0]](args.args)