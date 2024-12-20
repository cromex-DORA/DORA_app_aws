class GeoJSONRewind {

  rewindRing(ring, dir) {
      var area = 0, err = 0;
      for (var i = 0, len = ring.length, j = len - 1; i < len; j = i++) {
          var k = (ring[i][0] - ring[j][0]) * (ring[j][1] + ring[i][1]);
          var m = area + k;
          err += Math.abs(area) >= Math.abs(k) ? area - m + k : k - m + area;
          area = m;
      }
      if (area + err >= 0 !== !!dir) ring.reverse();
  }

  rewindRings(rings, outer) {
      if (rings.length === 0) return;

      this.rewindRing(rings[0], outer);
      for (var i = 1; i < rings.length; i++) {
          this.rewindRing(rings[i], !outer);
      }
  }

  rewind(gj, outer) {
      var type = gj && gj.type, i;

      if (type === 'FeatureCollection') {
          for (i = 0; i < gj.features.length; i++) this.rewind(gj.features[i], outer);

      } else if (type === 'GeometryCollection') {
          for (i = 0; i < gj.geometries.length; i++) this.rewind(gj.geometries[i], outer);

      } else if (type === 'Feature') {
          this.rewind(gj.geometry, outer);

      } else if (type === 'Polygon') {
          this.rewindRings(gj.coordinates, outer);

      } else if (type === 'MultiPolygon') {
          for (i = 0; i < gj.coordinates.length; i++) this.rewindRings(gj.coordinates[i], outer);
      }

      return gj;
  }
}

window.GeoJSONRewind = GeoJSONRewind;