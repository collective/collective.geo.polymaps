# Polymap view for folders and topics
from zope.interface import implements
from zope.component import getUtility
from Products.Five import BrowserView

from plone.registry.interfaces import IRegistry


from collective.geo.settings.interfaces import IGeoSettings, IGeoFeatureStyle

from collective.geo.polymaps.interfaces import IPolymapView

from utils import INLINE_STYLES, create_map_js

class PolymapView(BrowserView):
    implements(IPolymapView)

    def get_js(self):
        defaultsetting = getUtility(IRegistry).forInterface(IGeoSettings)
        zoom = int(defaultsetting.zoom)
        lat = 0
        lon = 0
        return create_map_js(self.context, zoom)


    @property
    def map_inline_css(self):
        """Return inline CSS for our map according to style settings.
        """
        geofeaturestyle = getUtility(IRegistry).forInterface(IGeoFeatureStyle)
        inline_css = ''
        for style in INLINE_STYLES:
            value = getattr(geofeaturestyle, INLINE_STYLES[style], None)
            if value:
                inline_css += "%s:%s;" % (style, value)
        return inline_css or None
