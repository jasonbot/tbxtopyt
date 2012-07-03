Create Skeleton PYT from a TBX
==============================

This Python toolbox (converttbx.pyt) will take any geoprocessing
toolbox file (.TBX) and create a corresponding stub .PYT with a
corresponding Python implementation of the tools with the original
parameters of original toolbox.

!!!!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!!!!!!!!
===================================================

THIS IS NOT A 100% AUTOMATED SOLUTION TO CREATING PYTS. You will
need to go in and look over the source before you use it. There
will be definite areas where you NEED to change the source of the
new PYT, and others where you'll need to do some sanity checking
to make sure the PYT's functionality is similar to your original
TBX.
