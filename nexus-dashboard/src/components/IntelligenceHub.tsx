import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Loader2, AlertTriangle, Info, MapPin, Gauge } from 'lucide-react';
import { useStore } from '../store/useStore';

export function IntelligenceHub() {
  const { incidents, isCrisis } = useStore();
  const lastIncident = incidents[incidents.length - 1];

  // LOGICAL FALLBACK: If we are in crisis mode but have no incident yet, we show the analyzer
  const showCrisisStats = isCrisis || incidents.length > 0;

  return (
    <div className="flex-1 flex flex-col min-h-0 space-y-6">
      {/* 1. MISSION ANALYTICS (Top Summary) */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-900/40 backdrop-blur-xl border border-white/5 rounded-3xl p-5 flex flex-col justify-between">
            <span className="text-[9px] font-black uppercase tracking-widest text-blue-500 mb-2 flex items-center gap-2">
                <Gauge size={12} /> Confidence Score
            </span>
            <div className="flex items-baseline gap-1">
                <span className="text-3xl font-black text-white">
                    {lastIncident && lastIncident.confidence_score ? Math.round(lastIncident.confidence_score * 100) : '0'}
                </span>
                <span className="text-sm font-bold text-blue-500/50">%</span>
            </div>
        </div>
        <div className="bg-slate-900/40 backdrop-blur-xl border border-white/5 rounded-3xl p-5 flex flex-col justify-between">
            <span className="text-[9px] font-black uppercase tracking-widest text-red-500 mb-2 flex items-center gap-2">
                <MapPin size={12} /> Threat Zone
            </span>
            <span className="text-xs font-black uppercase tracking-tight text-white leading-tight truncate">
                {lastIncident?.location || 'Awaiting Signal...'}
            </span>
        </div>
      </div>

      {/* 2. CORE INTELLIGENCE CENTER */}
      <div className="flex-1 min-h-0 bg-slate-950/40 backdrop-blur-3xl border border-white/5 rounded-[2.5rem] p-6 shadow-2xl flex flex-col overflow-hidden">
        <div className="flex justify-between items-center mb-6">
            <h2 className="text-sm font-black uppercase tracking-[0.4em] flex items-center gap-3">
                <Shield size={16} className="text-blue-500" />
                Incident Diagnostics
            </h2>
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.6)]" />
        </div>

        <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
            {!showCrisisStats ? (
                <div className="py-8 flex flex-col items-center justify-center text-slate-700 animate-in fade-in duration-500">
                    <AlertTriangle size={32} className="mb-3 opacity-20" />
                    <p className="text-[10px] font-black uppercase tracking-[0.2em] text-center">Sentry Grid: STANDBY</p>
                </div>
            ) : !lastIncident ? (
                <div className="py-8 flex flex-col items-center justify-center text-blue-500/50 animate-pulse">
                    <Loader2 size={32} className="animate-spin mb-3" />
                    <p className="text-[10px] font-black uppercase tracking-[0.3em] font-mono">Analyzing Heuristics...</p>
                </div>
            ) : (
                <AnimatePresence mode="wait">
                    <motion.div 
                        key={lastIncident.incident_id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-6"
                    >
                        {/* Active Protocol Banner */}
                        <div className="bg-blue-600/10 border border-blue-500/20 rounded-2xl p-5 flex gap-5 items-center">
                            <div className="p-3 bg-blue-600 rounded-xl shadow-lg shadow-blue-600/20 text-white">
                                <Info size={18} />
                            </div>
                            <div>
                                <p className="text-[10px] font-black uppercase tracking-widest text-blue-400">Tactical SOP Active</p>
                                <h4 className="text-sm font-bold uppercase tracking-tight text-white">{lastIncident.active_protocol}</h4>
                            </div>
                        </div>

                        <div className="bg-white/5 border border-white/5 rounded-3xl p-6">
                             <p className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-3">AI Perception Summary</p>
                             <p className="text-sm leading-relaxed text-slate-200">
                                 {lastIncident.description}
                             </p>
                             <div className="mt-4 pt-4 border-t border-white/5 flex gap-4">
                                 <div className="text-[10px] font-black uppercase tracking-widest px-3 py-1 bg-white/5 rounded-lg border border-white/5 text-slate-400">
                                     Severity: {lastIncident.severity}
                                 </div>
                                 <div className="text-[10px] font-black uppercase tracking-widest px-3 py-1 bg-white/5 rounded-lg border border-white/5 text-slate-400">
                                     Source: {lastIncident.incident_type}
                                 </div>
                             </div>
                        </div>
                    </motion.div>
                </AnimatePresence>
            )}
        </div>
      </div>
    </div>
  );
}
