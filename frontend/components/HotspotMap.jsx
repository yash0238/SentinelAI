"use client";

import { useEffect, useState, useMemo } from "react";
import Map, { Source, Layer, NavigationControl } from "react-map-gl";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { RISK_COLORS } from "@/lib/mock-data";

// CARTO Dark Matter fallback map style (100% free open tiles)
const CARTO_DARK_STYLE = {
  version: 8,
  sources: {
    "carto-dark": {
      type: "raster",
      tiles: [
        "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
        "https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
        "https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
        "https://d.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
      ],
      tileSize: 256,
      attribution: '&copy; OpenStreetMap &copy; CARTO',
    },
  },
  layers: [
    {
      id: "carto-dark-layer",
      type: "raster",
      source: "carto-dark",
      minzoom: 0,
      maxzoom: 22,
    },
  ],
};

export default function HotspotMap({ hotspots }) {
  const [mounted, setMounted] = useState(false);
  const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;

  useEffect(() => {
    setMounted(true);
  }, []);

  // Format data for GeoJSON source
  const geojson = useMemo(() => {
    if (!hotspots) return null;
    return {
      type: "FeatureCollection",
      features: hotspots.map((h) => ({
        type: "Feature",
        properties: {
          city: h.city,
          count: h.count,
          risk: h.risk,
          color: RISK_COLORS[h.risk] || RISK_COLORS.LOW,
        },
        geometry: {
          type: "Point",
          coordinates: [h.lng, h.lat],
        },
      })),
    };
  }, [hotspots]);

  if (!mounted) return <div className="w-full h-full bg-base-800 rounded-xl" />;

  const layerStyle = {
    id: "hotspots-layer",
    type: "circle",
    paint: {
      "circle-radius": [
        "interpolate",
        ["linear"],
        ["get", "count"],
        10, 10,
        150, 26,
      ],
      "circle-color": ["get", "color"],
      "circle-opacity": 0.8,
      "circle-stroke-width": 2,
      "circle-stroke-color": "#ffffff",
    },
  };

  // MapTiler dark style URL or CARTO dark fallback
  const mapStyle = token
    ? `https://api.maptiler.com/maps/dataviz-dark/style.json?key=${token}`
    : CARTO_DARK_STYLE;

  return (
    <div className="w-full h-full rounded-xl overflow-hidden border border-base-400 relative">
      <Map
        mapLib={maplibregl}
        initialViewState={{
          longitude: 78.9629,
          latitude: 20.5937,
          zoom: 4.2,
        }}
        mapStyle={mapStyle}
        reuseMaps
      >
        <NavigationControl position="bottom-right" />
        {geojson && (
          <Source id="hotspots" type="geojson" data={geojson}>
            <Layer {...layerStyle} />
          </Source>
        )}
      </Map>

      {/* Legend overlaid on map */}
      <div className="absolute top-4 left-4 glass-card px-3 py-2 border border-base-400/50 z-10">
        <p className="text-[0.65rem] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Risk Level</p>
        <div className="space-y-1">
          {Object.entries(RISK_COLORS).map(([risk, color]) => (
            <div key={risk} className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
              <span className="text-xs text-slate-300 font-medium">{risk}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
