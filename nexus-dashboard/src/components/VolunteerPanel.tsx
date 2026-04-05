import React from 'react';
import { Loader2, Activity } from 'lucide-react';
import { IncidentCard } from './IncidentCard';

interface Incident {
  incident_id: string;
  incident_type: string;
  severity: number;
  location: string;
  description: string;
}

interface VolunteerPanelProps {
  incidents: Incident[];
  onAccept: (id: string) => void;
  isLoading?: boolean;
}

export const VolunteerPanel: React.FC<VolunteerPanelProps> = ({ incidents, onAccept, isLoading }) => {
  if (isLoading && incidents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-slate-500 border-2 border-dashed border-slate-800 rounded-2xl">
        <Loader2 className="animate-spin mb-4" />
        <p className="font-bold uppercase tracking-widest text-xs">Scanning Local Frequencies...</p>
      </div>
    );
  }

  if (incidents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-slate-600 border-2 border-dashed border-slate-800 rounded-2xl">
        <Activity size={32} className="mb-4 opacity-50" />
        <p className="font-bold uppercase tracking-widest text-xs">No active incidents reported.</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-lg mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-white text-sm font-black uppercase tracking-[0.3em] flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
          Live Mission Feed
        </h2>
        <span className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">
           {incidents.length} Detected
        </span>
      </div>
      <div className="space-y-4">
        {incidents.map(inc => (
          <IncidentCard key={inc.incident_id} incident={inc} onAccept={onAccept} />
        ))}
      </div>
    </div>
  );
};
