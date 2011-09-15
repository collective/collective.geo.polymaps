#

INLINE_STYLES = {'width': 'map_width',
                 'height': 'map_height'}


def create_map_js(context, zoom =0, lon=0, lat=0):
    context_url = context.absolute_url()
    if not context_url.endswith('/'):
        context_url += '/'
    return """
/*<![CDATA[*/
$(document).ready(function() {
    var cgp = collective_geo_polymaps_ns;
    var po = org.polymaps;
    var cgp_map = po.map()
        .container(document.getElementById("cgpolymap").appendChild(po.svg("svg")))
        .center({lat: %(lat)f, lon: %(lon)f})
        .zoomRange([0, 18])
        .zoom(%(zoom)i)
        .add(po.interact());
    var layers = {
        'OpenStreetmap': po.image().url(
            po.url("http://{S}tile.openstreetmap.org" + "/{Z}/{X}/{Y}.png")
            .hosts(["a.","b.","c.",""])).id('11'),
        'Blue Marble' : po.image()
                .url("http://s3.amazonaws.com/com.modestmaps.bluemarble/{Z}-r{Y}-c{X}.jpg")
                .visible(false)
                .id('12')
    };
    cgp_map.add(layers["OpenStreetmap"]);
    cgp_map.add(layers["Blue Marble"]);
    cgp_map.add(po.geoJson()
        .url("%(url)s@@geo-json.json")
        .on("load", cgp.load));
    cgp_map.add(po.compass()
        .pan("none"));
    po.switcher(cgp_map, layers, {title : 'Base Layer'})
      .container(document.getElementById("layerswitcher"));
});
/*]]>*/
        """  %  {'url': context_url, 'lat': lat, 'lon':lon, 'zoom': zoom}
