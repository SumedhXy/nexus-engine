import React, { useState } from 'react';

interface EmergencyButtonProps {
  onTrigger: (content: string) => void;
}

export const EmergencyButton: React.FC<EmergencyButtonProps> = ({ onTrigger }) => {
  const [isSending, setIsSending] = useState(false);

  const handleSOS = async () => {
    // TACTICAL 1-CLICK: No manual prompt if already in crisis mission.
    // The engine automatically pulls the emergency number from your settings.
    setIsSending(true);
    try {
      // DEFAULT SIGNAL: The engine will now derive your identity from your Profile
      const finalSignal = "TACTICAL SOS ALERT: DISTRESS SIGNAL ACTIVE";
         
      await onTrigger(finalSignal);
      
      // Reset after success animation
      setTimeout(() => setIsSending(false), 3000);
    } catch {
      setIsSending(false);
    }
  };

  return (
    <div className="relative group">
        <div className="absolute -inset-2 bg-red-600 rounded-full blur-2xl opacity-10 group-hover:opacity-30 transition-opacity duration-500" />
        <button
            onClick={handleSOS}
            disabled={isSending}
            className={`relative w-24 h-24 rounded-full bg-[#f8272d] flex flex-col items-center justify-center text-white font-black shadow-[0_0_50px_rgba(248,39,45,0.5)] active:scale-[0.85] transition-all outline-none border-4 border-white/20 select-none ${
                !isSending ? 'animate-pulse hover:brightness-110' : 'animate-ping'
            }`}
        >
            <span className="text-[10px] uppercase opacity-70 tracking-widest leading-none mb-0.5 font-black">Hold</span>
            <span className="text-2xl leading-none brightness-125">SOS</span>
        </button>
    </div>
  );
};
