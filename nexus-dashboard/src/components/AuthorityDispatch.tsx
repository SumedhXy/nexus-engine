import { motion } from 'framer-motion';
import { Shield, AlertTriangle, Users, MapPin, CheckCircle2, ChevronRight, Clock } from 'lucide-react';
import { useStore } from '../store/useStore';

export function AuthorityDispatch() {
  const { activeCards, isCrisis } = useStore();

  return (
    <div className="flex-1 flex flex-col min-h-0 space-y-6">
      {/* 2. CORE AUTHORITY CENTER */}
      <div className="flex-1 min-h-0 bg-slate-950/40 backdrop-blur-3xl border border-white/5 rounded-[2.5rem] p-6 shadow-2xl flex flex-col overflow-hidden">
        <div className="flex justify-between items-center mb-6">
            <h2 className="text-sm font-black uppercase tracking-[0.4em] flex items-center gap-3">
                <Users size={16} className="text-blue-500" />
                Authority Roster
            </h2>
            <div className="flex items-center gap-2 px-3 py-1 bg-blue-500/10 border border-blue-500/30 rounded-full text-[9px] text-blue-500 font-black">
               {activeCards.length} UNITS DEPLOYED
            </div>
        </div>

        <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
            {!isCrisis && activeCards.length === 0 ? (
                <div className="py-12 flex flex-col items-center justify-center text-slate-700 animate-in fade-in duration-500">
                    <AlertTriangle size={32} className="mb-3 opacity-20" />
                    <p className="text-[10px] font-black uppercase tracking-[0.2em] text-center">Standby for Authority Assignment</p>
                </div>
            ) : activeCards.length === 0 ? (
                <div className="py-12 flex flex-col items-center justify-center text-blue-500/50 animate-pulse">
                    <div className="w-10 h-10 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin mb-4" />
                    <p className="text-[10px] font-black uppercase tracking-[0.3em] font-mono">Syncing Incident Grid...</p>
                </div>
            ) : (
                <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
                    {/* Public Safety Units */}
                    {activeCards.map(card => (
                        <motion.div 
                            key={card.card_id}
                            initial={{ opacity: 0, y: 30, scale: 0.95 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            className="bg-slate-900/40 backdrop-blur-xl border border-white/5 rounded-3xl p-6 shadow-2xl relative overflow-hidden"
                        >
                            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 blur-[50px] rounded-full -mr-10 -mt-10" />
                            
                            <div className="flex justify-between items-start relative z-10 mb-5">
                                <div className="flex gap-4">
                                    <div className="w-12 h-12 bg-blue-600/10 border border-blue-500/30 rounded-2xl flex items-center justify-center text-blue-500">
                                        <Shield size={24} />
                                    </div>
                                    <div>
                                        <div className="text-[10px] font-black uppercase tracking-[0.3em] text-blue-400 mb-1">Public Safety Organization</div>
                                        <h3 className="text-xl font-black uppercase tracking-wide leading-none">
                                            {card.role.split('_').map((w: string) => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                                        </h3>
                                    </div>
                                </div>
                                <div className="bg-blue-600/20 border border-blue-500/50 px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest text-blue-400">
                                    PRIORITY {card.priority}
                                </div>
                            </div>

                            <div className="space-y-4 relative z-10">
                                <div className="flex flex-col gap-2">
                                    <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Mission Directives</span>
                                    {card.actions.map((action, i) => (
                                        <div key={i} className="flex gap-4 items-start bg-white/5 p-4 rounded-2xl border border-white/5 hover:bg-white/[0.08] transition-colors">
                                            <CheckCircle2 size={16} className="text-blue-500 mt-0.5 shrink-0" />
                                            <p className="text-[13px] leading-relaxed text-slate-200 font-medium">{action}</p>
                                        </div>
                                    ))}
                                </div>
                                
                                <div className="mt-4 pt-4 border-t border-white/5 flex justify-between items-center text-[10px] font-black uppercase tracking-widest text-slate-500">
                                     <div className="flex items-center gap-2">
                                         <Clock size={12} />
                                         STATUS: DISPATCHED
                                     </div>
                                     <div className="flex items-center gap-2">
                                         <MapPin size={12} />
                                         UNIT ON ROUTE
                                     </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            )}
        </div>
      </div>
    </div>
  );
}
