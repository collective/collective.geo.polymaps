# Polymap view for folders and topics
from zope.interface import implements
from zope.component import getUtility
from Products.Five import BrowserView

from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import IFolderish

from collective.geo.settings.interfaces import IGeoSettings, IGeoFeatureStyle

from collective.geo.polymaps.interfaces import IPolymapView

from utils import INLINE_STYLES, create_map_js

class PolymapView(BrowserView):
    implements(IPolymapView)

    def get_js(self):
        return create_map_js(self.context, self.layers())


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

    def layers(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        _layers = [{'name': self.context.Title(),
                    'url': context_url + '/@@geo-json.json',
                    'id': self.context.getId()}]
        path = '/'.join(self.context.getPhysicalPath())
        query = {'query': path, 'depth': 1}
        for brain in self.context.portal_catalog(path=query,
                                object_provides=IFolderish.__identifier__):
            _layers.append({'name': brain.Title,
                            'url': brain.getURL() + '/@@geo-json.json',
                            'id': brain.getId})
        return _layers
