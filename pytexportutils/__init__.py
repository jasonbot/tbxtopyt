"""Type library collection pytexportutils"""
__version__ = '10.1'
__all__ = ['ArcGISVersion', 'esriSystem', 'esriSystemUI', 'esriGeometry', 'esriGraphicsCore', 'esriGraphicsSymbols', 'esriDisplay', 'esriGeoDatabase', 'esriGeoDatabaseDistributed', 'esriGeoDatabaseExtensions', 'esriGeoDatabasePS', 'esriDataSourcesFile', 'esriDataSourcesGDB', 'esriDataSourcesOleDB', 'esriDataSourcesRaster', 'esriDataSourcesNetCDF', 'esriDataSourcesRasterUI', 'esriCarto', 'esriGeoprocessing']
# Required by all submodules, if these get in a bad state the C modules will crash.
_IIDMap = {}
_CLSIDMap = {}
_RecordMap = {}

class Enumeration(object):
   "Base class for enumerations"
   @classmethod
   def valueFor(cls, value):
      """Look up the textual name for an integer representation of an
        enumeration value"""
      return ([x for x in cls.__slots__ 
              if getattr(cls, x) == value] or [None]).pop()
   __slots__ = []
   pass


def IndexProperty(getter=None, setter=None):
    "For getter/setters with an index argument"
    class IndexedPropertyGetter(object):
        def __init__(self, other):
            self._other = other
        def __setitem__(self, index, value):
            if setter is not None:
                return setter(self._other, index, value)
            raise TypeError("%s object does not support item assignment" % 
                            self._other.__class__.__name__)
        def __getitem__(self, index):
            if getter is not None:
                return getter(self._other, index)
            raise TypeError("%s object does not support indexing" % 
                            self._other.__class__.__name__)
    return property(IndexedPropertyGetter)


def FAILED(item):
    """Usage: FAILED(HRESULT or IFace)

       Indicates if the specified HRESULT indicates a failure or the last call
       on the specified interface instance failed."""
    hr = item
    if not isinstance(item, (int, long)):
        if hasattr(item, '_HR'):
            hr = item._HR
    if not isinstance(hr, (int, long)):
        raise ValueError(repr(hr))
    return bool(hr & 0x80000000)

def SUCCEEDED(item):
    """SUCCEEDED(HRESULT or IFace)

       Indicates if the specified HRESULT indicates a failure or the last call
       on the specified interface instance succeeded."""
    return not FAILED(item)

def interfaces_supported(interface_object):
    """Returns a list of Interface types in this packages supported by the 
       supplied COM object instance."""
    if not hasattr(interface_object, 'supports'):
        interface_object = IUnknown(interface_object) # coerce
    return [iface for iid, iface in _IIDMap.iteritems()
                  if interface_object.supports(iid)]

from .esriSystem import *
from .esriGeoDatabase import *
from .esriGeoprocessing import *
