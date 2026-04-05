import React, { useEffect, useState } from 'react';
import { MapContainer as LeafletMap, TileLayer, Marker, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { MapPin, Loader2, Navigation } from 'lucide-react';
import { useStore } from '../store/useStore';

// Fix Leaflet marker icon issue in React
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

const RecenterMap = ({ center }: { center: [number, number] }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, 14);
  }, [center, map]);
  return null;
};

export const MapContainer: React.FC = () => {
  const { setGPS } = useStore();
  const [center, setCenter] = useState<[number, number]>([28.6139, 77.2090]); // Delhi fallback
  const [hasLocation, setHasLocation] = useState(false);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const coords: [number, number] = [pos.coords.latitude, pos.coords.longitude];
          setCenter(coords);
          setGPS(coords);
          setHasLocation(true);
        },
        (err) => console.warn("Location access denied", err),
        { enableHighAccuracy: true }
      );
    }
  }, [setGPS]);

  return (
    <div className="w-full h-full bg-[#0a0a0a] rounded-[2.5rem] relative overflow-hidden border-[12px] border-black/10 shadow-2xl group">
      {!hasLocation && (
        <div className="absolute inset-0 z-[1000] bg-black/40 backdrop-blur-sm flex flex-col items-center justify-center gap-3">
          <Loader2 size={24} className="text-blue-500 animate-spin" />
          <span className="text-[10px] font-black uppercase text-white tracking-widest opacity-60">
            Acquiring Mission Location...
          </span>
        </div>
      )}

      <LeafletMap
        center={center}
        zoom={13}
        style={{ width: '100%', height: '100%', background: '#000' }}
        zoomControl={false}
        attributionControl={false}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        />
        <RecenterMap center={center} />
        <Marker position={center} />
      </LeafletMap>

      {/* Tactical HUD Overlay */}
      <div className="absolute top-6 left-6 z-[1000] flex flex-col gap-2 pointer-events-none">
        <div className="bg-black/80 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 flex items-center gap-3 shadow-xl">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-ping" />
            <span className="text-[10px] font-black uppercase text-white tracking-widest leading-none">
                Live Ops View: Active Tracking
            </span>
        </div>
        <div className="bg-blue-600/20 backdrop-blur-md px-3 py-1.5 rounded-lg border border-blue-500/20 flex items-center gap-2">
            <Navigation size={12} className="text-blue-400" />
            <span className="text-[10px] font-bold text-blue-400 tracking-tighter">
                {center[0].toFixed(5)}, {center[1].toFixed(5)}
            </span>
        </div>
      </div>

      {/* Map Branding Anchor */}
      <div className="absolute bottom-6 left-6 z-[1000] opacity-30 grayscale contrast-125 flex items-center gap-1">
        <MapPin size={10} className="text-white" />
        <span className="text-[8px] font-black text-white uppercase tracking-[0.3em]">NEXUS CARTOGRAPHY</span>
      </div>
    </div>
  );
};
