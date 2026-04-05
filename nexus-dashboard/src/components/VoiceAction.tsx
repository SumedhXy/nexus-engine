import React, { useState } from 'react';
import { Mic, Send, X } from 'lucide-react';

interface VoiceActionProps {
  onTrigger: (content: string) => void;
}

export const VoiceAction: React.FC<VoiceActionProps> = ({ onTrigger }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [text, setText] = useState('');

  const toggleRecording = () => {
    if (isRecording) {
      setIsRecording(false);
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech Recognition not supported in this browser. Try Chrome.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsRecording(true);
    recognition.onend = () => setIsRecording(false);
    
    recognition.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0])
        .map(result => result.transcript)
        .join('');
      setText(transcript);
    };

    recognition.onerror = (event: any) => {
      console.error("Speech Error:", event.error);
      setIsRecording(false);
    };

    recognition.start();
  };

  const handleSend = () => {
    if (!text.trim()) return;
    onTrigger(text);
    setText('');
  };

  return (
    <div className="flex-1 flex items-center bg-[#0a0f1a] border border-slate-800 rounded-2xl p-2 transition-all h-20 shadow-xl">
      <button
        onClick={toggleRecording}
        className={`p-4 rounded-xl transition-all ${
          isRecording ? 'bg-red-500 text-white animate-pulse' : 'text-blue-500 hover:bg-slate-800'
        }`}
      >
        <Mic size={24} />
      </button>
      
      <div className="flex-1 px-4 overflow-hidden relative">
        {isRecording ? (
          <span className="text-xs font-black text-red-500 animate-pulse uppercase tracking-[0.2em] block">
            Listening...
          </span>
        ) : (
          <input 
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Activate Voice SOS"
            className="w-full bg-transparent border-none outline-none text-slate-100 font-bold text-sm placeholder:text-slate-500 placeholder:font-bold h-full"
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
        )}
      </div>

      {(text || isRecording) && (
        <button
          onClick={text ? handleSend : () => setIsRecording(false)}
          className={`p-4 rounded-xl transition-all shadow-lg ${
            text ? 'bg-blue-600 text-white' : 'text-slate-600'
          }`}
        >
          {text ? <Send size={20} /> : <X size={20} />}
        </button>
      )}
    </div>
  );
};
