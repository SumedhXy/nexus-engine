import React from 'react';
import { Loader2, MapPin, AlertTriangle } from 'lucide-react';

interface Incident {
  incident_id: string;
  incident_type: string;
  severity: number;
  location: string;
  description: string;
}

interface IncidentCardProps {
  incident: Incident;
  onAccept: (id: string) => void;
  isAccepting?: boolean;
}

export const IncidentCard: React.FC<IncidentCardProps> = ({ incident, onAccept, isAccepting }) => {
  const severityColors: Record<number, string> = {
    1: 'bg-blue-500', 2: 'bg-green-500', 3: 'bg-yellow-500', 4: 'bg-orange-500', 5: 'bg-red-600'
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg mb-4 hover:border-nexus-blue/50 transition-all">
      <div className="flex justify-between items-start mb-3">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <AlertTriangle size={14} className="text-nexus-blue" />
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">
              {incident.incident_type}
            </span>
          </div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <MapPin size={18} className="text-red-500" />
            {incident.location}
          </h3>
        </div>
        <div className={`${severityColors[incident.severity]} px-3 py-1 rounded-full text-[10px] font-black text-white uppercase`}>
          Severity {incident.severity}
        </div>
      </div>
      
      <p className="text-slate-400 text-sm mb-5 leading-relaxed">
        {incident.description}
      </p>

      <button
        onClick={() => onAccept(incident.incident_id)}
        disabled={isAccepting}
        className="w-full bg-white text-black font-black py-3 rounded-lg flex items-center justify-center gap-2 hover:bg-slate-200 transition-colors uppercase text-sm disabled:bg-slate-700"
      >
        {isAccepting ? <Loader2 className="animate-spin" size={18} /> : 'Accept Mission'}
      </button>
    </div>
  );
};
