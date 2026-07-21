"use client";

import { useEffect, useState, useMemo } from "react";
import Map, { Source, Layer, NavigationControl } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { RISK_COLORS } from "@/lib/mock-data";

/**
 * HotspotMap — Mapbox GL map of active digital arrests.
 * If NEXT_PUBLIC_MAPBOX_TOKEN is missing, renders a CSS-only fallback map.
 */
export default function HotspotMap({ hotspots }) {
  const [mounted, setMounted] = useState(false);
  const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;

  useEffect(() => {
    setMounted(true);
  }, []);

  // Format data for Mapbox GeoJSON source
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
          // Used by Mapbox expressions for coloring
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

  // Mapbox missing fallback
  if (!token) {
    return (
      <div className="w-full h-full bg-base-700 rounded-xl border border-base-400 flex flex-col items-center justify-center p-6 text-center">
        <div className="w-16 h-16 rounded-full bg-base-600 flex items-center justify-center mb-4">
          <span className="text-2xl">🗺️</span>
        </div>
        <p className="text-slate-300 font-medium mb-1">
          Mapbox Token Required
        </p>
        <p className="text-sm text-slate-500 max-w-sm">
          To see the interactive map, add <code>NEXT_PUBLIC_MAPBOX_TOKEN</code> to your <code>.env.local</code> file and restart the server.
        </p>
        
        {/* Simple CSS visualization of the data */}
        <div className="mt-6 w-full max-w-md bg-base-800 rounded-lg p-4 border border-base-400 text-left">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Hotspots Data Preview
          </p>
          <div className="space-y-2">
            {hotspots?.slice(0, 5).map((h) => (
              <div key={h.city} className="flex items-center justify-between">
                <span className="text-sm text-slate-300">{h.city}</span>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium text-slate-400">{h.count} reports</span>
                  <span 
                    className="w-2.5 h-2.5 rounded-full" 
                    style={{ backgroundColor: RISK_COLORS[h.risk] }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const layerStyle = {
    id: "hotspots-layer",
    type: "circle",
    paint: {
      "circle-radius": [
        "interpolate",
        ["linear"],
        ["get", "count"],
        10, 8,
        150, 24,
      ],
      "circle-color": ["get", "color"],
      "circle-opacity": 0.6,
      "circle-stroke-width": 1,
      "circle-stroke-color": ["get", "color"],
    },
  };

  return (
    <div className="w-full h-full rounded-xl overflow-hidden border border-base-400 relative">
      <Map
        initialViewState={{
          longitude: 79.0,
          latitude: 22.0,
          zoom: 3.5,
          pitch: 25,
        }}
        mapStyle="mapbox://styles/mapbox/dark-v11"
        mapboxAccessToken={token}
      >
        <NavigationControl position="bottom-right" />
        {geojson && (
          <Source id="hotspots" type="geojson" data={geojson}>
            <Layer {...layerStyle} />
          </Source>
        )}
      </Map>
      
      {/* Legend overlaid on map */}
      <div className="absolute top-4 left-4 glass-card px-3 py-2 border border-base-400/50">
        <p className="text-[0.65rem] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Risk Level</p>
        <div className="space-y-1">
          {Object.entries(RISK_COLORS).map(([risk, color]) => (
            <div key={risk} className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
              <span className="text-xs text-slate-300">{risk}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
