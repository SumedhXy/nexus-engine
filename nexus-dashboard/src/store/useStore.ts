import { create } from 'zustand';
import { auth, googleProvider, signInWithPopup, signInAnonymously } from '../firebase';
import type { User } from 'firebase/auth';

export interface UserProfile {
  user_id: string;
  full_name: string;
  emergency_contact_number: string;
  medical_info?: string;
  blood_group?: string;
}

export interface Incident {
  incident_id: string;
  incident_type: string;
  severity: number;
  location: string;
  description: string;
  status: string;
  confidence_score?: number;
  active_protocol?: string;
}

export interface ActionCard {
  card_id: string;
  role: string;
  actions: string[];
  location: string;
  priority: number;
  status?: 'dispatched' | 'acknowledged' | 'complete';
}

interface NexusState {
  user: User | null;
  loading: boolean;
  profile: UserProfile | null;
  incidents: Incident[];
  activeCards: ActionCard[];
  isCrisis: boolean;
  connectivity: 'online' | 'offline';
  gps: [number, number];
  
  // Actions
  setProfile: (profile: UserProfile | null) => void;
  setUser: (user: User | null) => void;
  setIncidents: (incidents: Incident[]) => void;
  addIncident: (incident: Incident) => void;
  setActiveCards: (cards: ActionCard[]) => void;
  setPowerMode: (isCrisis: boolean) => void;
  setConnectivity: (status: 'online' | 'offline') => void;
  updateCardStatus: (id: string, status: ActionCard['status']) => void;
  setGPS: (gps: [number, number]) => void;
  
  // Auth Operations
  loginGoogle: () => Promise<void>;
  loginAnon: () => Promise<void>;
  logout: () => Promise<void>;
}

export const useStore = create<NexusState>((set) => ({
  user: null,
  loading: true,
  profile: null,
  incidents: [],
  activeCards: [],
  isCrisis: false,
  connectivity: 'online',
  gps: [0, 0],

  setProfile: (profile) => set({ profile }),
  setUser: (user) => set({ user, loading: false }),
  addIncident: (incident: Incident) => set((state) => ({ incidents: [...state.incidents, incident] })),
  setIncidents: (incidents) => set({ incidents }),
  setActiveCards: (activeCards) => set({ activeCards }),
  setPowerMode: (isCrisis) => set({ isCrisis }),
  setConnectivity: (status) => set({ connectivity: status }),
  setGPS: (gps) => set({ gps }),
  updateCardStatus: (id, status) => set((state) => ({
    activeCards: state.activeCards.map(c => c.card_id === id ? { ...c, status } : c)
  })),

  loginGoogle: async () => {
    try {
      await signInWithPopup(auth, googleProvider);
    } catch (e) {
      console.error("Google Auth Failed:", e);
    }
  },

  loginAnon: async () => {
    try {
      await signInAnonymously(auth);
    } catch (e) {
      console.error("Anon Auth Failed:", e);
    }
  },

  logout: async () => {
    await auth.signOut();
    set({ user: null, profile: null, incidents: [], activeCards: [], isCrisis: false });
  },
}));
