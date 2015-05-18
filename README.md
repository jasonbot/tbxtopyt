# TBX to PYT Translator

This Python toolbox (converttbx.pyt) will take any geoprocessing
toolbox file (.TBX) and create a corresponding stub .PYT with a
corresponding Python implementation of the tools with the original
parameters of original toolbox.

## Features
* Create Skeleton PYT from a TBX
* Basic conversion from geoprocessing toolbox (.tbx) to Python toolbox (.pyt).

## Requirements

* ArcGIS 10.1
* Some experience editing Python code
* Microsoft Visual Studio 2008 or [Microsoft Visual C++ Compiler for Python 2.7](http://www.microsoft.com/en-us/download/details.aspx?id=44266) (to compile the C extensions yourself if you go the build route)

## Instructions for Downloading (**recommended method**)

1. Download the [pre-built version from ArcGIS.com](http://www.arcgis.com/home/item.html?id=83585412edd04ae48bdffea3e1f7b2e7) and continue with the steps below for usage.

## Instructions for Building

1. Download and unzip the .zip file or clone the repo.
2. Build and install `pytexportutils`: `C:\Python27\ArcGIS10.2\python setup.py install`.
3. Continue with the instructions for using the toolbox.

## Instructions for Using (after downloading or building)

3. Open the provided converttbx.pyt inside of ArcCatalog or Catalog View.
4. Provide the existing .tbx file as input.
5. Examine and refine the resulting .pyt file.

 [New to Github? Get started here.](https://github.com/)

## Resources

* [Python for ArcGIS Resource Center](http://resources.arcgis.com/en/communities/python/)
* [Analysis and Geoprocessing Blog](http://blogs.esri.com/esri/arcgis/category/subject-analysis-and-geoprocessing/)
* [twitter@arcpy](http://twitter.com/arcpy)

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

# ! WARNING !

THIS IS NOT A 100% AUTOMATED SOLUTION TO CREATING PYTS. You will
need to go in and look over the source before you use it. There
will be areas where you NEED to change the source of the new PYT, 
and others where you'll need to do some sanity checking to make 
sure the PYT's functionality is similar to your original TBX.


## Contributing

Anyone and everyone is welcome to contribute. 

## Licensing
Copyright 2012 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's [license.txt](https://raw.github.com/Esri/switch-basemaps-js/master/license.txt) file.

[](Esri Tags: ArcGIS Toolboxes)
[](Esri Language: Python)
