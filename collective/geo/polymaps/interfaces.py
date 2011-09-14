from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class ICGPolymapsLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """

class IJsonPolymapsViewlet(Interface):
    """Marker interface for Viewlet"""

class IPolymapView(Interface):
     """Marker interface for View"""
