from zope.interface import implements
from zope.component import getUtility
from zope.component import queryAdapter
from shapely.geometry import asShape

from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry

from collective.geo.geographer.interfaces import IGeoreferenced

from collective.geo.settings.interfaces import (
                                        IGeoCustomFeatureStyle,
                                        IGeoFeatureStyle,
                                        IGeoSettings)

from collective.geo.polymaps.interfaces import IJsonPolymapsViewlet

INLINE_STYLES = {'width': 'map_width',
                 'height': 'map_height'}


class ContentViewlet(ViewletBase):
    implements(IJsonPolymapsViewlet)

    def get_js(self):
        defaultsetting = getUtility(IRegistry).forInterface(IGeoSettings)
        zoom = int(defaultsetting.zoom)
        context_url = self.context.absolute_url()
        shape = asShape(self.coordinates.geo)
        lat = shape.centroid.y
        lon = shape.centroid.x
        if not context_url.endswith('/'):
            context_url += '/'
        return """
        /*<![CDATA[*/

        var po = org.polymaps;

        var map = po.map()
            .container(document.getElementById("cgpolymap").appendChild(po.svg("svg")))
            .center({lat: %(lat)f, lon: %(lon)f})
            .zoomRange([1, 18])
            .zoom(%(zoom)i)
            .add(po.interact());

        map.add(po.image().url(
                  po.url("http://{S}tile.openstreetmap.org" + "/{Z}/{X}/{Y}.png")
                  .hosts(["a.","b.","c.",""])));

        map.add(po.geoJson()
            .url("%(url)s@@geo-json.json")
            .on("load", cgpolymap_load));

        // this must be called after layer creation otherwise it is not visible
        map.add(po.compass()
            .pan("none"));

        /*]]>*/
        """  %  {'url': context_url, 'lat': lat, 'lon':lon, 'zoom': zoom}



    def get_load_js(self):
        return


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
