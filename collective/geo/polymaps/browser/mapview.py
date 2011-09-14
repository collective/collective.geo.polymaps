# Polymap view for folders and topics
from zope.interface import implements
from zope.component import getUtility
from Products.Five import BrowserView

from plone.registry.interfaces import IRegistry

from collective.geo.settings.interfaces import IGeoSettings, IGeoFeatureStyle

from collective.geo.polymaps.interfaces import IPolymapView

INLINE_STYLES = {'width': 'map_width',
                 'height': 'map_height'}


class PolymapView(BrowserView):
    implements(IPolymapView)

    def get_js(self):
        defaultsetting = getUtility(IRegistry).forInterface(IGeoSettings)
        zoom = int(defaultsetting.zoom)
        context_url = self.context.absolute_url()
        lat = 0
        lon = 0
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
