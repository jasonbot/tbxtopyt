from distutils.core import setup, Extension

import arcpy

install_dir = arcpy.GetInstallInfo()['InstallDir']
com_dir = os.path.join(install_dir, 'com')

setup(
    name='pytexportutils',
    version='10.2',
    packages=['pytexportutils'],
    ext_package='pytexportutils',
    ext_modules=[
      Extension('_esriSystem',
                ['src/esriSystem.cpp'],
                include_dirs=[com_dir]),
      Extension('_esriGeoDatabase',
                ['src/esriGeoDatabase.cpp'],
                include_dirs=[com_dir]),
      Extension('_esriGeoprocessing',
                ['src/esriGeoprocessing.cpp'],
                include_dirs=[com_dir])
    ],
    package_data={'pytexportutils': ["./*.pdb"]}
)
