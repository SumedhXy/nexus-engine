import { useState, useEffect } from 'react';
import { Settings, LogOut, Loader2, Radio, Globe, BrainCircuit, Users, History } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { EmergencyButton } from './components/EmergencyButton';
import { VoiceAction } from './components/VoiceAction';
import { MapContainer } from './components/MapContainer';
import { ProfileModal } from './components/ProfileModal';
import { AuthGate } from './components/AuthGate';
import { IntelligenceHub } from './components/IntelligenceHub';
import { AuthorityDispatch } from './components/AuthorityDispatch';
import { MissionHistory } from './components/MissionHistory';
import { useStore } from './store/useStore';
import { api } from './api/client';
import { onAuthStateChanged, auth } from './firebase';

type TabType = 'field' | 'intel' | 'authority' | 'history';

function Dashboard() {
  const { user, profile, setProfile, logout, isCrisis, setActiveCards, setPowerMode, addIncident, gps } = useStore();
  const [activeTab, setActiveTab] = useState<TabType>('field');
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isLoadingProfile, setIsLoadingProfile] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    if (!user) return;
    const fetchProfile = async () => {
      try {
        const resp = await api.getProfile(user.uid);
        if (resp.data) setProfile(resp.data);
      } catch (err) {
        console.log("Onboarding required...");
      } finally {
        setIsLoadingProfile(false);
      }
    };
    fetchProfile();
  }, [user, setProfile]);

  const handleIncidentSubmit = async (content: string) => {
    if (!user) return;
    setIsProcessing(true);
    setPowerMode(true);
    
    // MISSION HEARTBEAT: Switch tab immediately to show "Analyzing"
    setActiveTab('intel');

    try {
      // TACTICAL METADATA: Pass live GPS coordinates for SMS Broadcast
      const gpsString = `${gps[0].toFixed(5)}, ${gps[1].toFixed(5)}`;
      const resp = await api.submitEmergency(content, user.uid, { gps: gpsString });
      console.log("📡 [NEXUS MISSION SIGNAL RECEIVED]:", resp.data);
      
      if (resp.data.incident) {
        const assignments = resp.data.dispatch?.assignments || [];
        
        // 1. ADD TO MISSION HISTORY
        addIncident({
           ...resp.data.incident,
           active_protocol: resp.data.sop?.name || 'Standard SOS Protocol',
           confidence_score: resp.data.incident.confidence_score,
           dispatch: resp.data.dispatch
        });
        
        // 2. MISSION LOCK: Short delay for store-sync stabilization
        setTimeout(() => {
          setPowerMode(true);
          setActiveTab('intel');
          
          // 3. SEQUENTIAL ROSTER REVEAL
          setActiveCards([]);
          assignments.forEach((card: any, index: number) => {
            setTimeout(() => {
                const currentCards = useStore.getState().activeCards;
                setActiveCards([...currentCards, card]);
            }, index * 400);
          });
        }, 100);
      }
    } catch (err: any) {
      console.error("❌ [NEXUS LITHIUM CRASH]: Mission capture failed.", err);
      setPowerMode(false); 
      setActiveTab('field');
      const errorMsg = err.response?.data?.detail?.error || err.response?.data?.detail || err.message;
      alert(`NEXUS LINK BROKEN: ${errorMsg}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClearIncident = () => {
    setPowerMode(false);
    setActiveCards([]);
    setActiveTab('field');
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans flex flex-col p-6 max-w-lg mx-auto overflow-hidden relative">
      <ProfileModal 
        isOpen={isProfileOpen || (!isLoadingProfile && !profile)} 
        onClose={() => setIsProfileOpen(false)}
        isOnboarding={!profile}
      />

      {/* Header */}
      <header className="flex justify-between items-center mb-10 pt-4">
        {!isCrisis ? (
          <button onClick={logout} className="text-slate-600 hover:text-red-500 transition-colors">
            <LogOut size={20} />
          </button>
        ) : (
          <button onClick={handleClearIncident} className="text-red-500 font-black uppercase text-[9px] tracking-widest bg-red-500/10 px-3 py-1.5 rounded-full border border-red-500/20 shadow-lg shadow-red-900/10 transition-all hover:bg-red-500 hover:text-white">
            End Mission
          </button>
        )}
        
        <h1 className="text-2xl font-black tracking-tighter uppercase text-slate-100 flex items-center gap-3">
            <div className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse" />
            NEXUS
        </h1>

        <div className="flex gap-4">
          <button onClick={() => setIsProfileOpen(true)} className="text-slate-400 hover:text-white transition-colors">
            <Settings size={22} />
          </button>
        </div>
      </header>

      {/* Dynamic Mission View */}
      <div className="flex-1 flex flex-col min-h-0 relative mb-24 transition-all">
        <AnimatePresence mode="wait">
            {activeTab === 'field' ? (
                <motion.div 
                    key="field"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                    className="flex-1 flex flex-col min-h-0"
                >
                    {isProcessing && (
                      <div className="absolute inset-0 z-[100] bg-black/80 backdrop-blur-md flex flex-col items-center justify-center rounded-[2.5rem] animate-in fade-in duration-300">
                        <Loader2 size={48} className="text-blue-500 animate-spin mb-4" />
                        <h2 className="text-sm font-black uppercase tracking-[0.3em]">Processing Heuristics</h2>
                      </div>
                    )}
                    <div className={`flex-1 overflow-hidden transition-all duration-700 rounded-[2.5rem] ${isCrisis ? 'h-56 shadow-2xl shadow-red-950/20 border-2 border-red-900/20' : 'mb-8 shadow-2xl shadow-blue-900/10 border border-white/5'}`}>
                      <MapContainer />
                    </div>
                    {!isCrisis && (
                        <div className="mt-auto pb-4 px-2">
                            <div className="flex justify-between items-start mb-6">
                                <div>
                                    <h2 className="text-2xl font-black mb-1 italic">
                                        {profile ? profile.full_name.split(' ')[0] : (user?.displayName ? user.displayName.split(' ')[0] : 'Operator')}
                                    </h2>
                                    <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest">SENTRY STATUS: GREEN</p>
                                </div>
                                <div className="flex items-center gap-2 px-3 py-1 bg-green-500/10 border border-green-500/30 rounded-full text-[9px] text-green-500 font-black">
                                    <Radio size={10} className="animate-pulse" /> ACTIVE
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                <VoiceAction onTrigger={handleIncidentSubmit} />
                                <EmergencyButton onTrigger={handleIncidentSubmit} />
                            </div>
                        </div>
                    )}
                </motion.div>
            ) : activeTab === 'intel' ? (
                <motion.div 
                    key="intel"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                    className="flex-1 flex flex-col min-h-0"
                >
                    <IntelligenceHub />
                </motion.div>
            ) : activeTab === 'authority' ? (
                <motion.div 
                    key="authority"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                    className="flex-1 flex flex-col min-h-0"
                >
                    <AuthorityDispatch />
                </motion.div>
            ) : (
                <motion.div 
                    key="history"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                    className="flex-1 flex flex-col min-h-0"
                >
                    <MissionHistory />
                </motion.div>
            )}
        </AnimatePresence>
      </div>

      {/* Floating Tactical Navigation */}
      <nav className="fixed bottom-8 inset-x-4 z-[2000] flex justify-center pointer-events-none">
        <div className="bg-slate-950/90 backdrop-blur-3xl border border-white/10 rounded-[2.5rem] p-1.5 flex gap-1 pointer-events-auto shadow-2xl shadow-black ring-1 ring-white/10">
            <button 
                onClick={() => setActiveTab('field')}
                className={`flex items-center gap-1.5 px-4 py-2.5 rounded-[1.8rem] transition-all duration-500 ${activeTab === 'field' ? 'bg-blue-600 text-white font-black shadow-lg shadow-blue-900/40' : 'text-slate-500 hover:bg-white/5 font-bold'}`}
            >
                <Globe size={14} />
                <span className="text-[9px] uppercase tracking-widest leading-none">Field</span>
            </button>
            <button 
                onClick={() => setActiveTab('intel')}
                className={`flex items-center gap-1.5 px-4 py-2.5 rounded-[1.8rem] transition-all duration-500 ${activeTab === 'intel' ? 'bg-blue-600 text-white font-black shadow-lg shadow-blue-900/40' : 'text-slate-500 hover:bg-white/5 font-bold'}`}
            >
                <BrainCircuit size={14} />
                <span className="text-[9px] uppercase tracking-widest leading-none">Intel</span>
            </button>
            <button 
                onClick={() => setActiveTab('authority')}
                className={`flex items-center gap-1.5 px-4 py-2.5 rounded-[1.8rem] transition-all duration-500 ${activeTab === 'authority' ? 'bg-blue-600 text-white font-black shadow-lg shadow-blue-900/40' : 'text-slate-500 hover:bg-white/5 font-bold'}`}
            >
                <Users size={14} />
                <span className="text-[9px] uppercase tracking-widest leading-none">Auth</span>
            </button>
            <button 
                onClick={() => setActiveTab('history')}
                className={`flex items-center gap-1.5 px-4 py-2.5 rounded-[1.8rem] transition-all duration-500 ${activeTab === 'history' ? 'bg-blue-600 text-white font-black shadow-lg shadow-blue-900/40' : 'text-slate-500 hover:bg-white/5 font-bold'}`}
            >
                <History size={14} />
                <span className="text-[9px] uppercase tracking-widest leading-none">Logs</span>
            </button>
        </div>
      </nav>
    </div>
  );
}

export default function App() {
  const { setUser } = useStore();
  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (user) => {
      setUser(user);
    });
    return () => unsub();
  }, [setUser]);

  return (
    <AuthGate>
      <Dashboard />
    </AuthGate>
  );
}
