import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { History, MapPin, Clock, ShieldAlert, ChevronRight } from 'lucide-react';
import { useStore } from '../store/useStore';
import { api } from '../api/client';

export const MissionHistory: React.FC = () => {
    const { user } = useStore();
    const [history, setHistory] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (!user) return;
        const fetchHistory = async () => {
            try {
                const resp = await api.getHistory(user.uid);
                setHistory(resp.data || []);
            } catch (err) {
                console.error("History fetch failed:", err);
            } finally {
                setIsLoading(false);
            }
        };
        fetchHistory();
    }, [user]);

    if (isLoading) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col min-h-0 space-y-4 px-2 overflow-y-auto pb-40 scrollbar-hide">
             <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-blue-600/10 border border-blue-500/20 rounded-xl">
                    <History size={18} className="text-blue-500" />
                </div>
                <div>
                   <h2 className="text-xl font-black uppercase tracking-tight">Mission History</h2>
                   <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">Archived Dispatch Logs</p>
                </div>
             </div>

             {history.length === 0 ? (
                <div className="bg-slate-900/50 border border-white/5 rounded-[2rem] p-10 text-center flex flex-col items-center gap-4">
                    <History size={48} className="text-slate-800" />
                    <p className="text-sm font-bold text-slate-500 uppercase tracking-widest">No Missions Recorded</p>
                </div>
             ) : (
                history.map((record, idx) => (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.1 }}
                        key={record.incident?.incident_id || idx}
                        className="group bg-slate-900/50 hover:bg-slate-900 border border-white/5 hover:border-blue-500/30 rounded-3xl p-5 transition-all duration-500"
                    >
                        <div className="flex justify-between items-start mb-4">
                            <div className="flex items-center gap-3">
                                <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-white ${
                                    record.incident?.severity >= 4 ? 'bg-red-600 shadow-lg shadow-red-900/20' : 'bg-slate-800'
                                }`}>
                                    <ShieldAlert size={20} />
                                </div>
                                <div>
                                    <h3 className="font-black uppercase tracking-tight text-sm leading-none mb-1">
                                        {record.incident?.incident_type?.toUpperCase() || 'GENERAL SOS'}
                                    </h3>
                                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-tighter">
                                        Mission: {record.incident?.incident_id?.substring(0, 8)}
                                    </p>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="text-[10px] font-black uppercase tracking-tighter text-blue-500 mb-1 flex items-center gap-1 justify-end">
                                    <Clock size={10} /> {new Date(record.incident?.timestamp).toLocaleTimeString()}
                                </p>
                                <p className="text-[9px] font-bold text-slate-600 uppercase tracking-tighter">
                                    {new Date(record.incident?.timestamp).toLocaleDateString()}
                                </p>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-3 mb-4">
                             <div className="bg-black/40 rounded-2xl p-3 border border-white/5 flex flex-col justify-center">
                                <div className="flex items-center gap-2 mb-1">
                                    <MapPin size={12} className="text-slate-500" />
                                    <span className="text-[9px] font-black uppercase text-slate-500 tracking-widest leading-none">GPS Fix</span>
                                </div>
                                <span className="text-[10px] font-black text-slate-300 leading-none">
                                    {record.incident?.location || '28.6139, 77.2090'}
                                </span>
                             </div>
                             <div className="bg-black/40 rounded-2xl p-3 border border-white/5 flex flex-col justify-center">
                                <div className="flex items-center gap-2 mb-1">
                                    <History size={12} className="text-slate-500" />
                                    <span className="text-[9px] font-black uppercase text-slate-500 tracking-widest leading-none">Status</span>
                                </div>
                                <span className="text-[10px] font-black text-green-500 leading-none uppercase">
                                    Dispatched
                                </span>
                             </div>
                        </div>

                        <div className="flex items-center justify-between group-hover:px-2 transition-all">
                             <span className="text-[10px] font-bold text-slate-400 italic">
                                Action: {record.incident?.description?.substring(0, 30)}...
                             </span>
                             <ChevronRight size={16} className="text-slate-700 group-hover:text-blue-500 transition-colors" />
                        </div>
                    </motion.div>
                ))
             )}
        </div>
    );
};
