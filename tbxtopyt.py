import arcpy

import imp
import os
import re

__all__ = ['export_tbx_to_pyt']

mod_find = imp.find_module('pytexportutils', [os.path.abspath(os.path.dirname(__file__))])
pytexportutils = imp.load_module('pytexportutils', *mod_find)

ACCEPTABLE_VARIABLENAME = re.compile("^[_a-z][_a-z0-9]*$", re.IGNORECASE)
CALL_RE_TEMPLATE = "((?:[_a-z][_a-z0-9]* *[.] *)*{}\(([^)]*)\))"
CODING_RE = re.compile("coding: ([^ ]+)", re.IGNORECASE)
HEADER_SOURCE = """# -*- coding: utf-8 -*-

import contextlib
import os
import sys

import arcpy

# You can ignore/delete this code; these are basic utility functions to
# streamline porting

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

def set_parameter_as_text(params, index, val):
    if (hasattr(params[index].value, 'value')):
        params[index].value.value = val
    else:
        params[index].value = val
"""

FUNCTION_REMAPPINGS = (
    ('AddMessage', 'messages.AddMessage({})'),
    ('AddWarning', 'messages.AddWarningMessage({})'),
    ('AddError', 'messages.AddErrorMessage({})'),
    ('AddIDMessage', 'messages.AddIDMessage({})'),
    ('GetParameterAsText', 'parameters[{}].valueAsText'),
    ('SetParameterAsText', 'set_parameter_as_text(parameters, {})'),
    ('GetParameter', 'parameters[{}]'),
    ('GetArgumentCount', 'len(parameters)'),
    ('GetParameterInfo', 'parameters')
)

def collect_lines(fn):
    def fn_(*args, **kws):
        return '\n'.join(fn(*args, **kws))
    return fn_

def rearrange_source(source, indentation):
    source = source.replace("\r\n", "\n").replace("\t", "    ")
    # Guess coding?
    if '\n' in source:
        id1 = source.find('\n')
        if '\n' in source[id1+1:]:
            id1 = source.find('\n', id1 + 1)
        match_obj = CODING_RE.findall(source[:id1])
        if match_obj:
            source = source.decode(match_obj[0])
        else:
            try:
                source = source.decode("utf-8")
            except:
                pass
    src = "\n".join("{}{}".format(" " * indentation,
                                  line.encode("utf-8"))
                                  for line in source.split("\n"))
    # Now apply some mechanical translations to common parameter access routines
    for fnname, replacement_pattern in FUNCTION_REMAPPINGS:
        regexp = re.compile(CALL_RE_TEMPLATE.format(fnname), re.IGNORECASE)
        finds = regexp.findall(src)
        if finds:
            for codepattern, arguments in finds:
                src = src.replace(codepattern, replacement_pattern.format(arguments))
    return src

class Tool(object):
    def __init__(self, tool_object):
        self._tool = tool_object
        param_list = self._tool.ParameterInfo
        self._parameters = [pytexportutils.IGPParameter(param_list.Element[idx])
                            for idx in xrange(param_list.Count)]
    @property
    def name(self):
        try:
            if ACCEPTABLE_VARIABLENAME.match(self._tool.Name):
                return self._tool.Name
        except:
            pass
        return "Tool{}".format(hex(id(self))[2:])
    @property
    @collect_lines
    def python_code(self):
        yield "class {}(object):".format(self.name)
        yield '    """{}"""'.format(self._tool.PathName.encode("utf-8"))

        try:
            gptool = pytexportutils.IGPScriptTool2(self._tool)
            codeblock = gptool.CodeBlock.encode("utf-8").replace("__init__(self)", "__init__(self, parameters)")
            yield rearrange_source(codeblock, 4)
        except:
            pass

        yield "    def __init__(self):"
        try:
            yield "        self.label = {}".format(repr(self._tool.DisplayName))
        except:
            pass
        try:
            yield "        self.description = {}".format(repr(self._tool.Description))
        except:
            pass
        try:
            yield "        self.canRunInBackground = {}".format(not pytexportutils.IGPScriptTool2(self._tool).RunInProc)
        except:
            yield "        self.canRunInBackground = False"
        yield "    def getParameterInfo(self):"
        index_dict = {parameter.Name.lower(): idx for idx, parameter in enumerate(self._parameters)}
        for idx, parameter in enumerate(self._parameters):
            yield "        # {}".format(parameter.Name.encode("utf-8"))
            yield "        param_{} = arcpy.Parameter()".format(idx + 1)
            yield "        param_{}.name = {}".format(idx + 1, repr(parameter.Name))
            yield "        param_{}.displayName = {}".format(idx + 1, repr(parameter.DisplayName))
            yield "        param_{}.parameterType = {}".format(idx + 1, 
                                                               repr(pytexportutils.esriGPParameterType.valueFor(parameter.ParameterType)
                                                                                        [len('esriGPParameterType'):]))
            yield "        param_{}.direction = '{}'".format(idx + 1, 
                                                             "Output" if (parameter.Direction ==
                                                                          pytexportutils.esriGPParameterDirection
                                                                                        .esriGPParameterDirectionOutput) else "Input")
            if (parameter.DataType.supports(pytexportutils.IGPMultiValueType.IID)):
                yield "        param_{}.datatype = {}".format(idx + 1, repr(pytexportutils.IGPMultiValueType(parameter.DataType).MemberDataType.DisplayName))
                yield "        param_{}.multiValue = True".format(idx + 1)
            elif (parameter.DataType.supports(pytexportutils.IGPCompositeDataType.IID)):
                cv = pytexportutils.IGPCompositeDataType(parameter.DataType)
                yield "        param_{}.datatype = {}".format(idx + 1, repr(tuple(cv.DataType[x].DisplayName for x in xrange(cv.Count))))
            elif (parameter.DataType.supports(pytexportutils.IGPValueTableType.IID)):
                vt = pytexportutils.IGPValueTableType(parameter.DataType)
                tablecols = [(vt.DataType[colindex].DisplayName, vt.DisplayName[colindex]) for colindex in xrange(vt.Count)]
                yield "        param_{}.columns = {}".format(idx + 1, repr(tablecols))
            else:
                yield "        param_{}.datatype = {}".format(idx + 1, repr(parameter.DataType.DisplayName))
            # default value
            try:
                value = parameter.Value.GetAsText()
                if value:
                    yield "        param_{}.value = {}".format(idx + 1, repr(value))
            except:
                pass

            # .filter.list
            try:
                cvd = pytexportutils.IGPCodedValueDomain(parameter.Domain)
                cvd_list = [cvd.Value[domainidx].GetAsText() for domainidx in xrange(cvd.CodeCount)]
                yield "        param_{}.filter.list = {}".format(idx + 1, repr(cvd_list))
            except:
                pass

            # .parameterDependencies
            try:
                deps = parameter.ParameterDependencies
                keep_going = True
                dep_list = []
                try:
                    while keep_going:
                        dep_list.append(index_dict.get(deps.Next().lower(), 0))
                        if not dep_list[-1]:
                            keep_going = False
                            dep_list = dep_list[:-1]
                except:
                    pass
                if dep_list:
                    yield "        param_{}.parameterDependencies = {}".format(idx + 1, repr(dep_list))
            except:
                pass
            yield ""
        yield "        return [{}]".format(", ".join("param_{}".format(idx + 1) for idx in xrange(len(self._parameters))))
        yield "    def isLicensed(self):"
        yield "        return True"
        yield "    def updateParameters(self, parameters):"
        yield "        validator = getattr(self, 'ToolValidator', None)"
        yield "        if validator:"
        yield "             return validator(parameters).updateParameters()"
        yield "    def updateMessages(self, parameters):"
        yield "        validator = getattr(self, 'ToolValidator', None)"
        yield "        if validator:"
        yield "             return validator(parameters).updateMessages()"
        yield "    def execute(self, parameters, messages):"
        try:
            filename = pytexportutils.IGPScriptTool(self._tool).FileName
            if os.path.isfile(filename):
                file_contents = open(filename, 'rb').read()
                yield "        with script_run_as({}):".format(repr(filename))
                yield rearrange_source(file_contents, 12)
            else:
                yield "        # {}".format(repr(filename))
                try:
                    # Coerce as source?
                    compile(filename, self._tool.PathName, "exec")
                    yield "        with script_run_as({}):".format(repr(self._tool.PathName))
                    yield rearrange_source(filename, 12)
                except:
                    pass
        except:
            yield "        pass"

class PYTToolbox(object):
    def __init__(self, tbx_name):
        gpu = pytexportutils.IGPUtilities(pytexportutils.GPUtilities())
        name = gpu.GetNameObjectFromLocation(tbx_name)
        assert name, "Could not find {}".format(tbx_name)
        new_object = name.Open()
        assert new_object, "could not open toolbox"
        assert new_object.supports(pytexportutils.IGPToolbox.IID), "{} is not a toolbox".format(tbx_name)
        self._toolbox = pytexportutils.IGPToolbox(new_object)
        self._tools = map(Tool, iter(self._toolbox.Tools.Next, None))
    @property
    @collect_lines
    def python_code(self):
        yield "# Export of toolbox {}".format(self._toolbox.PathName.encode("utf-8"))
        yield ""
        yield "import arcpy"
        yield ""
        yield "class Toolbox(object):"
        yield "    def __init__(self):"
        tbx_name = os.path.splitext(os.path.basename(self._toolbox.PathName))[0]
        try:
            tbx_name = pytexportutils.IGPToolbox2(self._toolbox).DisplayName
        except:
            pass
        yield "        self.label = {}".format(repr(tbx_name))
        alias = ""
        try:
            alias = self._toolbox.Alias
        except:
            pass
        yield "        self.alias = {}".format(repr(alias))
        yield "        self.tools = [{}]".format(", ".join(t.name for t in self._tools))
        yield ""
        yield "# Tool implementation code"
        for tool in self._tools:
            yield ""
            yield tool.python_code

def export_tbx_to_pyt(in_tbx, out_file):
    toolbox = PYTToolbox(in_tbx)
    with open(out_file, 'wb') as out:
        out.write(HEADER_SOURCE)
        out.write('\n')
        out.write(toolbox.python_code)

if __name__ == "__main__":
    import glob
    #[r'C:\SupportFiles\ArcGIS\ArcToolBox\Toolboxes\Spatial Statistics Tools.tbx']: #[r'Toolboxes\My Toolboxes\OutScript.tbx']:
    for filename in [os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.tbx")]:
        print HEADER_SOURCE
        print PYTToolbox(filename).python_code.encode("ascii", "replace")
