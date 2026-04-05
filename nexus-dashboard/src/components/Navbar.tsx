import React from 'react';
import { Shield, Wifi, WifiOff, Zap, LayoutDashboard } from 'lucide-react';
import { useStore } from '../store/useStore';

export const Navbar: React.FC = () => {
  const { connectivity, isCrisis } = useStore();

  return (
    <nav className="fixed top-0 inset-x-0 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-nexus-blue rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Shield className="text-white" size={18} />
          </div>
          <span className="text-white font-black tracking-tighter text-xl">NEXUS</span>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 px-3 py-1 bg-slate-800 rounded-full">
            {connectivity === 'online' ? (
              <Wifi size={14} className="text-green-500" />
            ) : (
              <WifiOff size={14} className="text-red-500" />
            )}
            <span className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">
              {connectivity}
            </span>
          </div>

          <div className={`flex items-center gap-2 px-3 py-1 rounded-full transition-all ${isCrisis ? 'bg-red-500/20 text-red-500 text-pulse-fast' : 'bg-slate-800 text-slate-400'}`}>
            <Zap size={14} />
            <span className="text-[10px] font-bold uppercase tracking-widest">
              {isCrisis ? 'Crisis Mode' : 'Sentry Mode'}
            </span>
          </div>
          
          <button className="text-slate-400 hover:text-white transition-colors">
            <LayoutDashboard size={20} />
          </button>
        </div>
      </div>
    </nav>
  );
};
