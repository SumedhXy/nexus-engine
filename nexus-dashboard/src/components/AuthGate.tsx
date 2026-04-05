import React, { useState } from 'react';
import { Shield, Lock, ChevronRight, Globe, Loader2, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { auth, googleProvider, signInWithPopup } from '../firebase';
import { useStore } from '../store/useStore';

interface AuthGateProps {
  children: React.ReactNode;
}

export const AuthGate: React.FC<AuthGateProps> = ({ children }) => {
  const { user, setUser } = useStore();
  const [status, setStatus] = useState<'idle' | 'linking' | 'success'>('idle');
  const [error, setError] = useState<string | null>(null);

  const handleGoogleLogin = async () => {
    setStatus('linking');
    setError(null);
    try {
      const result = await signInWithPopup(auth, googleProvider);
      
      // MISSION-CRITICAL: Capture official ID Token for backend validation
      const idToken = await result.user.getIdToken();
      localStorage.setItem('nexus_token', idToken);
      
      setStatus('success');
      // TACTICAL DISPATCH: Delay for high-fidelity confirmation
      setTimeout(() => setUser(result.user), 1800);
    } catch (err: any) {
      console.error("❌ [IDENTITY CRASH]:", err);
      setError("DASHBOARD LINK FAILED: Verify your Firebase configuration.");
      setStatus('idle');
    }
  };

  const handleQuickAccess = () => {
    setStatus('linking');
    // TACTICAL BYPASS: Grant access as a Guest Operator for immediate mission needs
    const guestUser: any = {
       uid: 'guest-operator-' + Math.random().toString(36).substring(7),
       displayName: 'Guest Operator',
       isAnon: true
    };
    
    // GUEST TOKEN: High-intensity mock token for local-mode bypass
    localStorage.setItem('nexus_token', 'GUEST_MISSION_SIGNAL_BYPASS');
    
    setTimeout(() => {
        setStatus('success');
        setTimeout(() => setUser(guestUser), 1000);
    }, 800);
  };

  if (user) return <>{children}</>;

  return (
    <div className="min-h-screen bg-[#050505] text-white flex flex-col items-center justify-center p-8 relative overflow-hidden font-sans">
      {/* Tactical Background Elements */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-900/10 blur-[120px] rounded-full" />
          <div className="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-[0.03]" />
          {status === 'success' && <div className="absolute inset-0 bg-green-500/5 transition-colors duration-1000" />}
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md relative z-10 text-center"
      >
        <div className="mb-12 inline-block">
            <div className={`w-20 h-20 rounded-3xl flex items-center justify-center mx-auto border transition-all duration-700 ${
                status === 'success' ? 'bg-green-600 shadow-[0_0_50px_rgba(34,197,94,0.4)] border-green-400' : 'bg-blue-600 shadow-[0_0_50px_rgba(37,99,235,0.3)] border-white/20'
            }`}>
                <Shield size={40} className="text-white" />
            </div>
            <h1 className="text-5xl font-black tracking-tighter uppercase mt-6 mb-2 italic italic-heavy">NEXUS</h1>
            <p className="text-[10px] font-black uppercase tracking-[0.5em] text-slate-500">Crisis Orchestration Hub</p>
        </div>

        <div className="min-h-[200px] flex flex-col justify-center">
            <AnimatePresence mode="wait">
                {status === 'linking' ? (
                   <motion.div 
                        key="linking"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 1.1 }}
                        className="space-y-6"
                   >
                        <div className="flex flex-col items-center gap-4">
                            <Loader2 size={32} className="text-blue-500 animate-spin" />
                            <div className="space-y-1">
                                <p className="text-[10px] font-black uppercase tracking-[0.3em] text-blue-500">Identity Handshake</p>
                                <h2 className="text-xl font-black uppercase tracking-tight">Synchronizing...</h2>
                            </div>
                        </div>
                        <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                            <motion.div 
                                initial={{ x: '-100%' }}
                                animate={{ x: '100%' }}
                                transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                                className="w-full h-full bg-blue-600 shadow-[0_0_10px_rgba(37,99,235,0.8)]"
                            />
                        </div>
                   </motion.div>
                ) : status === 'success' ? (
                    <motion.div 
                        key="success"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-green-600/10 border border-green-500/20 p-8 rounded-[2rem] flex flex-col items-center gap-4 backdrop-blur-xl"
                    >
                        <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-black shadow-lg shadow-green-500/30">
                            <CheckCircle2 size={36} />
                        </div>
                        <div className="space-y-1">
                           <p className="text-[10px] font-black uppercase tracking-[0.4em] text-green-500 leading-none mb-1">Access Granted</p>
                           <h2 className="text-2xl font-black uppercase tracking-tighter">Link Established</h2>
                        </div>
                    </motion.div>
                ) : (
                    <motion.div key="idle" exit={{ opacity: 0, y: -20 }} className="space-y-4">
                        {error && (
                            <div className="bg-red-500/10 border border-red-500/20 p-3 rounded-2xl text-[10px] font-black uppercase tracking-widest text-red-500 mb-6 animate-pulse">
                                {error}
                            </div>
                        )}

                        <button 
                            onClick={handleGoogleLogin}
                            className="w-full bg-white text-black h-16 rounded-[1.5rem] font-black uppercase tracking-widest flex items-center justify-center gap-3 transition-all hover:scale-[1.02] active:scale-95 shadow-xl shadow-white/5 group"
                        >
                            <Globe size={18} className="text-blue-600 group-hover:rotate-180 transition-transform duration-700" />
                            SIGN IN WITH MISSION ID
                        </button>

                        <button 
                            onClick={handleQuickAccess}
                            className="w-full bg-slate-900/50 backdrop-blur-xl border border-white/5 text-white h-16 rounded-[1.5rem] font-black uppercase tracking-widest flex items-center justify-center gap-3 transition-all hover:bg-white/5 active:scale-95 group"
                        >
                            QUICK MISSION ACCESS
                            <ChevronRight size={18} className="text-slate-600 group-hover:translate-x-1 transition-transform duration-300" />
                        </button>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>

        <div className="mt-16 flex items-center justify-center gap-8 text-[11px] font-black uppercase tracking-widest text-slate-700">
             <div className="flex items-center gap-2">
                 <Lock size={12} /> ENCRYPTED
             </div>
             <div className="flex items-center gap-2">
                 <Shield size={12} /> CLASS-IV
             </div>
        </div>
      </motion.div>
    </div>
  );
};
