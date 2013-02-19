# TBX to PYT Translator

This Python toolbox (converttbx.pyt) will take any geoprocessing
toolbox file (.TBX) and create a corresponding stub .PYT with a
corresponding Python implementation of the tools with the original
parameters of original toolbox.

## Features
* Create Skeleton PYT from a TBX
* Basic conversion from geoprocessing toolbox (.tbx) to Python toolbox (.pyt).

## Instructions

1. Download and unzip the .zip file or clone the repo.
2. Open the provided converttbx.pyt inside of ArcCatalog or Catalog View.
3. Provide the existing .tbx file as input.
4. Examine and refine the resulting .pyt file.

 [New to Github? Get started here.](https://github.com/)

## Requirements

* ArcGIS 10.1
* Some experience editing Python code

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
[](Esri Language: Python
