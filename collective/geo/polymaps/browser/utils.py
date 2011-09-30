#

INLINE_STYLES = {'width': 'map_width',
                 'height': 'map_height'}


def create_map_js(context, layers, zoom =0, lon=0, lat=0):
    context_url = context.absolute_url()
    if not context_url.endswith('/'):
        context_url += '/'
    vlt = """
    '%(name)s': po.geoJson().url("%(url)s").on("load", cgp.load).id("%(id)s")"""
    vectorlayers = []
    for layer in layers:
        vectorlayers.append(
        vlt % layer)
    vectorlayer_js = ','.join(vectorlayers)
    jlt = """
        cgp_map.add(vectorlayers["%(name)s"]);
        """
    jsonlayer_js = ''
    for layer in layers:
        jsonlayer_js += jlt % layer

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
    var baselayers = {
        'OpenStreetmap': po.image().url(
            po.url("http://{S}tile.openstreetmap.org" + "/{Z}/{X}/{Y}.png")
            .hosts(["a.","b.","c.",""])).id('11'),
        'Blue Marble' : po.image()
                .url("http://s3.amazonaws.com/com.modestmaps.bluemarble/{Z}-r{Y}-c{X}.jpg")
                .visible(false)
                .id('12')
    };
    cgp_map.add(baselayers["OpenStreetmap"]);
    cgp_map.add(baselayers["Blue Marble"]);
    var vectorlayers = {
    %(vectorlayer)s
    };
    %(jsonlayer)s
    cgp_map.add(po.compass()
        .pan("none"));
    po.switcher(cgp_map, baselayers, {title : 'Base Layer'})
      .container(document.getElementById("layerswitcher"));
    po.toggler(cgp_map, vectorlayers, {title : 'Vector Layers'})
      .container(document.getElementById("layertoggler"));
});
/*]]>*/
        """  %  {'jsonlayer': jsonlayer_js, 'vectorlayer': vectorlayer_js, 'lat': lat, 'lon':lon, 'zoom': zoom}
