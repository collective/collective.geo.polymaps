from zope.interface import implements
from zope.component import getUtility
from zope.component import queryAdapter
from shapely.geometry import asShape

from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry

from collective.geo.geographer.interfaces import IGeoreferenced
from collective.geo.settings.interfaces import (
                                        IGeoCustomFeatureStyle,
                                        IGeoFeatureStyle,
                                        IGeoSettings)

from collective.geo.polymaps.interfaces import IJsonPolymapsViewlet
from utils import INLINE_STYLES, create_map_js




class ContentViewlet(ViewletBase):
    implements(IJsonPolymapsViewlet)

    def get_js(self):
        defaultsetting = getUtility(IRegistry).forInterface(IGeoSettings)
        zoom = int(defaultsetting.zoom)
        shape = asShape(self.coordinates.geo)
        lat = shape.centroid.y
        lon = shape.centroid.x
        return create_map_js(self.context, self.layers())


    @property
    def coordinates(self):
        return IGeoreferenced(self.context)

    @property
    def geofeaturestyle(self):
        self.custom_styles = queryAdapter(self.context, IGeoCustomFeatureStyle)
        self.defaultstyles = getUtility(IRegistry).forInterface(IGeoFeatureStyle)
        if self.custom_styles and self.custom_styles.use_custom_styles:
            return self.custom_styles
        else:
            return self.defaultstyles

    @property
    def map_inline_css(self):
        """Return inline CSS for our map according to style settings.
        """
        inline_css = ''
        for style in INLINE_STYLES:
            value = getattr(self.geofeaturestyle, INLINE_STYLES[style], None)
            if value:
                inline_css += "%s:%s;" % (style, value)
        return inline_css or None

    @property
    def map_viewlet_position(self):
        return self.geofeaturestyle.map_viewlet_position


    def render(self):
        if 'polymaps:' + self.manager.__name__ != self.map_viewlet_position:
            return u''
        coords = self.coordinates
        if coords.type and coords.coordinates:
            return super(ContentViewlet, self).render()
        else:
            return ''

    def layers(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        return [{'name': self.context.Title(),
                'url': context_url + '@@geo-json.json',
                'id': self.context.getId()}]

class JSViewlet(ViewletBase):

    @property
    def portal_url(self):
        return getToolByName(self.context, 'portal_url')()
