# -*- coding: utf-8 -*-

import contextlib
import os
import sys

import arcpy

@contextlib.contextmanager
def script_run_as(filename, args=None):
    oldpath = sys.path[:]
    oldargv = sys.argv[:]
    newdir = os.path.dirname(filename)
    sys.path = oldpath + [newdir]
    sys.argv = [filename] + [arg.valueAsText for arg in (args or [])]
    oldcwd = os.getcwdu()
    os.chdir(newdir)

    try:
        # Actually run
        yield filename
    finally:
        # Restore old settings
        sys.path = oldpath
        sys.argv = oldargv
        os.chdir(oldcwd)

class Toolbox(object):
    def __init__(self):
        self.label = u'Convert to PYT'
        self.alias = u'pytmaker'
        self.tools = [CreatePYT]

# Tool implementation code

class CreatePYT(object):
    def __init__(self):
        self.label = u'Create PYT Template from TBX'
        self.description = u'Create a new PYT skeleton from the structure and parameters of an ArcGIS Toolbox (TBX) file.'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Input_Toolbox
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Toolbox'
        param_1.displayName = u'Input Toolbox'
        param_1.dataType = u'Toolbox'
        param_1.parameterType = 'Required'

        # Output_File
        param_2 = arcpy.Parameter()
        param_2.name = u'Output_File'
        param_2.displayName = u'Output File'
        param_2.dataType = u'File'
        param_2.parameterType = 'Required'

        return [param_1, param_2]
    def isLicensed(self):
        return True
    def updateParameters(self, parameters):
        if parameters[0].valueAsText and (not (parameters[1].valueAsText or parameters[1].altered)):
            if os.path.isdir(os.path.dirname(parameters[0].valueAsText)):
                newnamepart = os.path.splitext(parameters[0].valueAsText)[0]
                newnamepart += u"_converted.pyt"
                parameters[1].value = newnamepart
        pass
    def updateMessages(self, parameters):
        pass
    def execute(self, parameters, messages):
        with script_run_as(__file__):
            import tbxtopyt
            if not parameters[1].valueAsText.lower().endswith('.pyt'):
                parameters[1].value = parameters[1].valueAsText + ".pyt"
            tbxtopyt.export_tbx_to_pyt(parameters[0].valueAsText, parameters[1].valueAsText)
