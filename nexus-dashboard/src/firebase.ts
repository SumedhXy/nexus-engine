import { initializeApp, getApps } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, onAuthStateChanged, signOut, signInAnonymously } from 'firebase/auth';
import { getDatabase } from 'firebase/database';

const firebaseConfig = {
  apiKey: "AIzaSyBV0Sp1K6jv08Km22CbefCjcS5RpzdWaWA",
  authDomain: "nexus-system-d9078.firebaseapp.com",
  databaseURL: "https://nexus-system-d9078-default-rtdb.firebaseio.com",
  projectId: "nexus-system-d9078",
  storageBucket: "nexus-system-d9078.firebasestorage.app",
  messagingSenderId: "470112106116",
  appId: "1:470112106116:web:28828d19a93a41f43ef4d1",
  measurementId: "G-2L8077L1XZ"
};

// Initialize Firebase High-Fidelity
let app;
if (!getApps().length) {
  app = initializeApp(firebaseConfig);
} else {
  app = getApps()[0];
}

export const auth = getAuth(app);
export const db = getDatabase(app);
export const googleProvider = new GoogleAuthProvider(); // TACTICAL IDENTITY LINK

export { signInWithPopup, onAuthStateChanged, signOut, signInAnonymously };
