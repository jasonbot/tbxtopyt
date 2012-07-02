import arcpy

import imp
import os
import re

mod_find = imp.find_module('pytexportutils', [os.path.abspath(os.path.dirname(__file__))])
pytexportutils = imp.load_module('pytexportutils', *mod_find)

acceptable_variablename = re.compile("^[_a-z][_a-z0-9]*$", re.IGNORECASE)
coding_re = re.compile("coding: ([^ ]+)")

def collect_lines(fn):
    def fn_(*args, **kws):
        return '\n'.join(fn(*args, **kws))
    return fn_

def rearrange_source(source, indentation):
    source = source.replace("\r\n", "\n")
    # Guess coding?
    if '\n' in source:
        id1 = source.find('\n')
        if '\n' in source[id1+1:]:
            id1 = source.find('\n', id1 + 1)
        match_obj = coding_re.findall(source[:id1])
        if match_obj:
            source = source.decode(match_obj[0])
        else:
            try:
                source = source.decode("utf-8")
            except:
                pass
    return "\n".join("{}{}".format(" " * indentation,
                                   line.encode("utf-8"))
                      for line in source.split("\n"))

class Tool(object):
    def __init__(self, tool_object):
        self._tool = tool_object
    @property
    def name(self):
        try:
            if acceptable_variablename.match(self._tool.Name):
                return self._tool.Name
        except:
            pass
        return "Tool{}".format(hex(id(self))[2:])
    @property
    @collect_lines
    def python_code(self):
        yield "class {}(object):".format(self.name)
        yield '    """{}"""'.format(self._tool.PathName.encode("utf-8"))
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
            pass
        yield "    def getParameterInfo(self):"
        yield "        pass"
        yield "    def isLicensed(self):"
        yield "        pass"
        yield "    def updateParameters(self, parameters):"
        yield "        pass"
        yield "    def updateMessages(self, parameters):"
        yield "        pass"
        yield "    def execute(self, parameters, messages):"
        try:
            filename = pytexportutils.IGPScriptTool(self._tool).FileName
            if os.path.isfile(filename):
                file_contents = open(filename, 'rb').read()
                yield "        with fakefile({}):".format(repr(filename))
                yield rearrange_source(file_contents, 12)
            else:
                yield "        # {}".format(repr(filename))
                try:
                    # Coerce as source?
                    compile(filename, self._tool.PathName, "exec")
                    yield "        with fakefile({}):".format(repr(self._tool.PathName))
                    yield rearrange_source(filename, 12)
                except:
                    pass
        except Exception as e:
            yield "        pass # {}".format(e)

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
        yield "# -*- coding: utf-8 -*-"
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

if __name__ == "__main__":
    import glob
    for filename in glob.glob(r"c:\SupportFiles\ArcGIS\ArcToolbox\Toolboxes\Spatial*.tbx"):
        print filename
        print PYTToolbox(filename).python_code.encode("ascii", "replace")
