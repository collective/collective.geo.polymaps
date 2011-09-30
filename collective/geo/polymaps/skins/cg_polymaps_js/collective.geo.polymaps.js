if (!org) var org = {};
if (!org.polymaps) org.polymaps = {};

(function(po) {
  po.toggler = function(m, l, o) {
    var self = {},
        map,
        layers,
        options;

    map = m;
    layers = l;
    options = o ? o : {};
    if (!options.title) options.title = 'Vector Layers';

    /* toggle layer */
    self.toggle = function (name) {
        var l = layers[name];
        if (!l.map()) {
            map.add(l);
            l.visible(true);
        }
        var visible = l.visible();
        l.visible(!visible);
    }

    self.container = function (elt) {
        // Create Legend manipulating the DOM
        var main = elt;
        var list = document.createElement('div');
        list.setAttribute('id', 'togglelayer-list');
        // For each layer, create a <input>
        for (name in layers) {
            var layerid = layers[name].id();
            var input = document.createElement('input');
            input.setAttribute('id', 'togglelayer-' + layerid);
            input.setAttribute('name', 'togglelayer');
            input.setAttribute('type', 'checkbox');
            input.setAttribute('value', name);
            if (layers[name].map() && layers[name].visible()) input.setAttribute('checked', '');

            // Link onChange event on radio
            input.onchange = function () {
                self.toggle(this.getAttribute('value'));
            };
            var label = document.createElement('label');
            label.setAttribute('for', 'togglelayer-' + layerid);
            label.innerHTML = name;

            var item = document.createElement('div');
            item.appendChild(input);
            item.appendChild(label);
            list.appendChild(item);
        }
        var title = document.createElement('div');
        title.setAttribute('id', 'togglelayer-title');
        title.innerHTML = options.title;
        main.appendChild(title);
        main.appendChild(list);
        return self;
    }

    return self;
  };
  /*-------------*/
  po.switcher = function(m, l, o) {
    var self = {},
        map,
        layers,
        current,
        options;

    map = m;
    layers = l;
    options = o ? o : {};
    if (!options.title) options.title = 'Base Layer';

    /* switch to layer */
    self.switchto = function (name) {
        var l = layers[name];
        if (l.map()) {
            l.visible(true);
        }
        else {
            map.add(l);
        }
        if (current) {
            current.visible(false);
        }
        current = l;
    }

    self.container = function (elt) {
        // Create Legend manipulating the DOM
        var main = elt;
        var list = document.createElement('div');
        list.setAttribute('id', 'switcher-list');
        // For each layer, create a <input>
        for (name in layers) {
            var layerid = layers[name].id();
            var input = document.createElement('input');
            input.setAttribute('id', 'switcher-' + layerid);
            input.setAttribute('name', 'switcher-radio');
            input.setAttribute('type', 'radio');
            input.setAttribute('value', name);
            if (layers[name].map() && layers[name].visible()) input.setAttribute('checked', '');

            // Link onChange event on radio
            input.onchange = function () {
                self.switchto(this.getAttribute('value'));
            };
            var label = document.createElement('label');
            label.setAttribute('for', 'switcher-' + layerid);
            label.innerHTML = name;

            var item = document.createElement('div');
            item.appendChild(input);
            item.appendChild(label);
            list.appendChild(item);
        }
        var title = document.createElement('div');
        title.setAttribute('id', 'switcher-title');
        title.innerHTML = options.title;
        main.appendChild(title);
        main.appendChild(list);
        return self;
    }

    return self;
  };
})(org.polymaps);


var collective_geo_polymaps_ns = new function() {
    /* http://stackoverflow.com/questions/881515/javascript-namespace-declaration */
    var inital_load = true;
    var po = org.polymaps;

    function bounds(features) {
      var i = -1,
          n = features.length,
          geometry,
          bounds = [{lon: Infinity, lat: Infinity}, {lon: -Infinity, lat: -Infinity}];
      while (++i < n) {
        geometry = features[i].data.geometry;
        boundGeometry[geometry.type](bounds, geometry.coordinates);
      }
      return bounds;
    };

    function boundPoint(bounds, coordinate) {
      var x = coordinate[0], y = coordinate[1];
      if (x < bounds[0].lon) bounds[0].lon = x;
      if (x > bounds[1].lon) bounds[1].lon = x;
      if (y < bounds[0].lat) bounds[0].lat = y;
      if (y > bounds[1].lat) bounds[1].lat = y;
    };

    function boundPoints(bounds, coordinates) {
      var i = -1, n = coordinates.length;
      while (++i < n) boundPoint(bounds, coordinates[i]);
    };

    function boundMultiPoints(bounds, coordinates) {
      var i = -1, n = coordinates.length;
      while (++i < n) boundPoints(bounds, coordinates[i]);
    };

    var boundGeometry = {
      Point: boundPoint,
      MultiPoint: boundPoints,
      LineString: boundPoints,
      MultiLineString: boundMultiPoints,
      Polygon: function(bounds, coordinates) {
        boundPoints(bounds, coordinates[0]); // exterior ring
      },
      MultiPolygon: function(bounds, coordinates) {
        var i = -1, n = coordinates.length;
        while (++i < n) boundPoints(bounds, coordinates[i][0]);
      }
    };


    this.load = function(e) {
      var map = this.map();
      for (var i = 0; i < e.features.length; i++) {
        var feature = e.features[i];
        feature.element.setAttribute("id", feature.data.id);

       if(feature.data.geometry.type == 'Point') {
                /* set marker image*/
                /*
                var ICONSIZE = 16;
                var circle = $(feature.element);
                var root = circle.parent();
                img = root.add("svg:image")
                    .attr('width', ICONSIZE)
                    .attr('height', ICONSIZE)
                    .attr("transform", circle.attr('transform')
                            + ' translate(-'+(ICONSIZE/2)+','
                            + '-'+(ICONSIZE/2)+')');
                root.remove(circle);
                img.attr('xlink:href', feature.data.properties.style.image);
                */
            if(feature.data.properties.style.fill != null) {
                feature.element.setAttribute("style",
                "stroke: #" + feature.data.properties.style.stroke.substring(0,6) +';' +
                "stroke-opacity: " + (parseInt(feature.data.properties.style.stroke.substring(6,8),16) / 255) +'; ' +
                "stroke-width: " + feature.data.properties.style.width +'px;' +
                "fill: #" + feature.data.properties.style.fill.substring(0,6) +';' +
                "fill-opacity:" + (parseInt(feature.data.properties.style.fill.substring(6,8),16) / 255) +';'
                );
            };
         };

        if (feature.data.geometry.type.indexOf('Polygon') > -1){
            if(feature.data.properties.style.fill != null) {
                feature.element.setAttribute("style",
                "stroke: #" + feature.data.properties.style.stroke.substring(0,6) +';' +
                "stroke-opacity: " + (parseInt(feature.data.properties.style.stroke.substring(6,8),16) / 255) +'; ' +
                "stroke-width: " + feature.data.properties.style.width +'px;' +
                "fill: #" + feature.data.properties.style.fill.substring(0,6) +';' +
                "fill-opacity:" + (parseInt(feature.data.properties.style.fill.substring(6,8),16) / 255) +';'
                );
            };
        };

        if (feature.data.geometry.type.indexOf('Line') > -1){
            if(feature.data.properties.style.stroke != null) {
                feature.element.setAttribute("style",
                "stroke: #" + feature.data.properties.style.stroke.substring(0,6) +';' +
                "stroke-opacity: " + (parseInt(feature.data.properties.style.stroke.substring(6,8),16) / 255) +'; ' +
                "stroke-width: " + feature.data.properties.style.width +';'
                );
            };
        };

        feature.element.setAttribute("class", feature.data.properties.classes);

        feature.element.appendChild(po.svg("title").appendChild(
              document.createTextNode(feature.data.properties.title)).parentNode);

        feature.element.appendChild(po.svg("description").appendChild(
              document.createTextNode(feature.data.properties.description)).parentNode);

        feature.element.appendChild(po.svg("link").appendChild(
              document.createTextNode(feature.data.properties.url)).parentNode);
         $(feature.element).click(function( objEvent ){
            createPopup(this, objEvent);
            }) ;

      };
      if (inital_load && (e.features.length >0)) {
        map.extent(bounds(e.features)).zoomBy(-.5);
        inital_load = false;
      };
    };

    /***************************/
    //@Author: Adrian "yEnS" Mato Gondelle
    //@website: www.yensdesign.com
    //@email: yensamg@gmail.com
    //@license: Feel free to use it, but keep this credits please!
    /***************************/


    var popupStatus = 0;
    function loadPopup(){
        if(popupStatus==0){
            $("#backgroundPopup").css({
                "opacity": "0.5"
            });
            $("#backgroundPopup").fadeIn("slow");
            $("#popup-map-feature").fadeIn("slow");
            popupStatus = 1;
        }
    };

    function disablePopup(){
        if(popupStatus==1){
            $("#backgroundPopup").fadeOut("slow");
            $("#popup-map-feature").fadeOut("slow");
            popupStatus = 0;
        }
    };

    function centerPopup(e){
        $("#popup-map-feature").css({
            "position": "fixed",
            "top":  e.clientY  +"px",
            "left": e.clientX  +"px"
        });
    };


    function createPopup(e, evt){
        var title = e.childNodes[0].childNodes[0].wholeText;
        var desc = e.childNodes[1].childNodes[0].wholeText;
        var url = e.childNodes[2].childNodes[0].wholeText;
        $('#cgmptitle').html(title);
        $('p#cgmpcontent').html(desc);
        $('a#cgmplink').attr('href', url);
        centerPopup(evt);
        loadPopup();
    };

    $(document).ready(function(){
        $("#popup-map-featureClose").click(function(){
            disablePopup();
        });
        $("#backgroundPopup").click(function(){
            disablePopup();
        });
        $(document).keypress(function(e){
            if(e.keyCode==27 && popupStatus==1){
                disablePopup();
            }
        });

    });

};
