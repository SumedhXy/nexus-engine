import React, { useState, useEffect } from 'react';
import { X, Save, User, Phone, Activity, Heart } from 'lucide-react';
import { useStore } from '../store/useStore';
import type { UserProfile } from '../store/useStore';
import { api } from '../api/client';

interface ProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  isOnboarding?: boolean;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({ isOpen, onClose, isOnboarding = false }) => {
  const { user, profile, setProfile } = useStore();
  const [formData, setFormData] = useState<Partial<UserProfile>>({
    full_name: '',
    emergency_contact_number: '',
    medical_info: '',
    blood_group: '',
  });
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (profile) setFormData(profile);
  }, [profile]);

  if (!isOpen || !user) return null;

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      const fullProfile = { ...formData, user_id: user.uid } as UserProfile;
      await api.setProfile(user.uid, fullProfile);
      setProfile(fullProfile);
      onClose();
    } catch (err) {
      console.error("Failed to save profile:", err);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div 
      className="fixed inset-0 z-[2000] flex items-center justify-center p-4 bg-black/80 backdrop-blur-xl animate-in fade-in duration-300"
      onClick={onClose}
    >
      <div 
        className="bg-slate-900 border border-slate-800 w-full max-w-md rounded-3xl overflow-hidden shadow-2xl animate-in zoom-in-95 duration-300"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="bg-slate-800/50 p-6 flex justify-between items-center border-b border-slate-700/50">
          <div className="flex items-center gap-4">
            {user.photoURL ? (
                <img src={user.photoURL} alt="Avatar" className="w-12 h-12 rounded-2xl border-2 border-white/10 shadow-lg shadow-black/40" />
            ) : (
                <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center text-white border-2 border-white/10 shadow-lg shadow-black/40">
                    <User size={24} />
                </div>
            )}
            <div>
                <h2 className="text-xl font-black uppercase tracking-widest text-white leading-tight">
                    {isOnboarding ? 'Initialize Profile' : 'Tactical Settings'}
                </h2>
                <div className="flex flex-col">
                    <p className="text-[9px] font-black text-blue-500 uppercase tracking-widest">Authenticated: {user.email || 'GUEST-SESSION'}</p>
                    <p className="text-[8px] font-bold text-slate-500 uppercase tracking-tighter opacity-50">
                        ID: {user.uid}
                    </p>
                </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSave} className="p-6 space-y-5">
          <div className="space-y-1.5">
            <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest ml-1">Full Identity</label>
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
              <input
                required
                value={formData.full_name}
                onChange={e => setFormData({ ...formData, full_name: e.target.value })}
                placeholder="John Doe"
                className="w-full bg-black/40 border border-slate-700 rounded-2xl py-3.5 pl-12 pr-4 text-sm font-bold text-white focus:border-blue-500 transition-all outline-none"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest ml-1">Emergency Contact (SMS)</label>
            <div className="relative">
              <Phone className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
              <input
                required
                type="tel"
                value={formData.emergency_contact_number}
                onChange={e => setFormData({ ...formData, emergency_contact_number: e.target.value })}
                placeholder="+1 234 567 890"
                className="w-full bg-black/40 border border-slate-700 rounded-2xl py-3.5 pl-12 pr-4 text-sm font-bold text-white focus:border-blue-500 transition-all outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest ml-1">Blood Group</label>
              <div className="relative">
                <Heart className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                <input
                  value={formData.blood_group}
                  onChange={e => setFormData({ ...formData, blood_group: e.target.value })}
                  placeholder="O+"
                  className="w-full bg-black/40 border border-slate-700 rounded-2xl py-3.5 pl-12 pr-4 text-sm font-bold text-white focus:border-blue-500 transition-all outline-none"
                />
              </div>
            </div>
            <div className="space-y-1.5">
              <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest ml-1">Medical Condition</label>
              <div className="relative">
                <Activity className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                <input
                  value={formData.medical_info}
                  onChange={e => setFormData({ ...formData, medical_info: e.target.value })}
                  placeholder="Allergies, etc."
                  className="w-full bg-black/40 border border-slate-700 rounded-2xl py-3.5 pl-12 pr-4 text-sm font-bold text-white focus:border-blue-500 transition-all outline-none"
                />
              </div>
            </div>
          </div>

          <button
            disabled={isSaving}
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-black uppercase tracking-widest py-4 rounded-2xl transition-all shadow-xl shadow-blue-900/40 flex items-center justify-center gap-2 mt-4"
          >
            {isSaving ? 'Syncing...' : <><Save size={18} /> Save Profile</>}
          </button>
        </form>
      </div>
    </div>
  );
};
