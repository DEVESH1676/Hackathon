import React, { useState } from "react";
import { Button } from "../ui/button";

interface TicketFormProps {
  onSubmit: (title: string, description: string) => void;
  isLoading: boolean;
}

const TicketForm: React.FC<TicketFormProps> = ({ onSubmit, isLoading }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title && description) {
      onSubmit(title, description);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest ml-1">
          Subject
        </label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="e.g. VPN connection failing with error 619"
          disabled={isLoading}
          className="w-full bg-white/[0.03] border border-white/10 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all disabled:opacity-50"
        />
      </div>

      <div className="space-y-2">
        <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest ml-1">
          Description
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Provide technical context, error codes, and affected systems..."
          disabled={isLoading}
          rows={5}
          className="w-full bg-white/[0.03] border border-white/10 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all resize-none disabled:opacity-50"
        />
      </div>

      <Button 
        type="submit" 
        disabled={isLoading || !title || !description}
        className={`w-full h-14 rounded-2xl font-bold uppercase tracking-widest transition-all duration-500 ${
          isLoading 
            ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30" 
            : "bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 text-white shadow-lg shadow-cyan-500/20"
        }`}
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Processing Intelligence...
          </span>
        ) : (
          "Launch Pipeline Ignition"
        )}
      </Button>
    </form>
  );
};

export default TicketForm;
