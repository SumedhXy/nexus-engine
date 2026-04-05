import React from 'react';
import { CheckCircle, Clock, ShieldCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ActionCard {
  card_id: string;
  role: string;
  actions: string[];
  location: string;
  priority: number;
}

interface ActionCardFeedProps {
  cards: ActionCard[];
  onComplete: (id: string) => void;
}

export const ActionCardFeed: React.FC<ActionCardFeedProps> = ({ cards, onComplete }) => {
  return (
    <div className="fixed right-6 top-24 w-80 space-y-4 pointer-events-none">
      <AnimatePresence>
        {cards.map((card) => (
          <motion.div
            key={card.card_id}
            initial={{ x: 300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 300, opacity: 0 }}
            className="bg-slate-900/90 backdrop-blur border-l-4 border-l-nexus-blue border-r border-t border-b border-slate-800 rounded-lg p-4 shadow-2xl pointer-events-auto"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-black uppercase text-nexus-blue tracking-[0.2em] flex items-center gap-1">
                <ShieldCheck size={12} />
                {card.role}
              </span>
              <div className="flex items-center gap-1 text-[10px] text-slate-500">
                <Clock size={10} />
                Now
              </div>
            </div>
            
            <h4 className="text-white font-bold text-sm mb-3 underline decoration-nexus-blue/30 underline-offset-4">
              {card.location}
            </h4>
            
            <ul className="space-y-2 mb-4">
              {card.actions.map((action, i) => (
                <li key={i} className="text-xs text-slate-300 flex gap-2">
                  <span className="text-nexus-blue font-bold">»</span>
                  {action}
                </li>
              ))}
            </ul>

            <button
              onClick={() => onComplete(card.card_id)}
              className="w-full flex items-center justify-center gap-2 py-2 bg-slate-800 hover:bg-green-600/20 hover:text-green-500 transition-all rounded text-[10px] font-bold uppercase tracking-widest border border-slate-700"
            >
              <CheckCircle size={14} />
              Mark Phase Complete
            </button>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};
