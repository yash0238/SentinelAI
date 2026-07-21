"use client";

import { useState, useRef } from "react";
import VerdictCard from "@/components/VerdictCard";
import { analyzeText, analyzeAudio, analyzeImage } from "@/lib/api";
import { MessageSquare, Mic, Image as ImageIcon, Upload, Send } from "lucide-react";

export default function DemoPage() {
  const [mode, setMode] = useState("text"); // "text", "audio", "image"
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Text state
  const defaultText =
    "Sir, this is Inspector Sharma from CBI. Your Aadhaar is linked to a money laundering case. You are under digital arrest. Do not disconnect this call or share it with anyone. Transfer the amount for verification immediately or a warrant will be issued.";
  const [text, setText] = useState(defaultText);

  // File state (audio/image)
  const fileInputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleModeChange = (newMode) => {
    setMode(newMode);
    setResult(null);
    setFile(null);
    setPreview(null);
  };

  const handleFileSelect = (e) => {
    const selected = e.target.files?.[0];
    if (!selected) return;
    
    setFile(selected);
    setResult(null);

    // Create preview
    if (mode === "image" && selected.type.startsWith("image/")) {
      const url = URL.createObjectURL(selected);
      setPreview(url);
    } else if (mode === "audio" && selected.type.startsWith("audio/")) {
      const url = URL.createObjectURL(selected);
      setPreview(url);
    }
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      let res;
      if (mode === "text") {
        if (!text.trim()) return;
        res = await analyzeText(text);
      } else if (mode === "audio") {
        if (!file) return;
        res = await analyzeAudio(file);
      } else if (mode === "image") {
        if (!file) return;
        res = await analyzeImage(file);
      }
      setResult(res);
    } catch (err) {
      console.error(err);
      // Fallback is handled in the API client, but just in case
      alert("Analysis failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full flex flex-col space-y-6 animate-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <span className="text-2xl">🔬</span> Live Threat Analysis
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Submit a suspicious message, voice note, or currency note image. SentinelAI returns an explainable, multi-modal verdict.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Column */}
        <div className="flex flex-col gap-5">
          {/* Mode Selector */}
          <div className="flex bg-base-800 p-1.5 rounded-xl border border-base-400 self-start">
            <button
              onClick={() => handleModeChange("text")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                mode === "text" ? "bg-base-600 text-slate-100 shadow-sm" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              <MessageSquare className="w-4 h-4" /> Text / Transcript
            </button>
            <button
              onClick={() => handleModeChange("audio")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                mode === "audio" ? "bg-base-600 text-slate-100 shadow-sm" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              <Mic className="w-4 h-4" /> Voice Note
            </button>
            <button
              onClick={() => handleModeChange("image")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                mode === "image" ? "bg-base-600 text-slate-100 shadow-sm" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              <ImageIcon className="w-4 h-4" /> Currency Note
            </button>
          </div>

          {/* Input Area */}
          <div className="glass-card p-6 flex flex-col gap-4 border-t-2" style={{ borderTopColor: '#4da6ff' }}>
            
            {mode === "text" && (
              <>
                <label className="text-sm font-bold text-slate-300 uppercase tracking-wider">
                  Message Content
                </label>
                <textarea
                  className="textarea-field"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Paste suspicious text here..."
                />
              </>
            )}

            {(mode === "audio" || mode === "image") && (
              <>
                <div className="flex items-center justify-between">
                  <label className="text-sm font-bold text-slate-300 uppercase tracking-wider">
                    {mode === "audio" ? "Upload Voice Note" : "Upload Image"}
                  </label>
                  <p className="text-xs text-slate-500 bg-base-800 px-2 py-1 rounded">
                    Tip: Filenames with "fake" or "synthetic" trigger positive hits in demo mode.
                  </p>
                </div>
                
                <div 
                  className="border-2 border-dashed border-base-400 rounded-xl p-8 flex flex-col items-center justify-center gap-3 bg-base-800/50 hover:bg-base-800 transition-colors cursor-pointer"
                  onClick={() => fileInputRef.current?.click()}
                >
                  {preview ? (
                    mode === "image" ? (
                      <img src={preview} alt="Preview" className="max-h-48 rounded object-contain" />
                    ) : (
                      <div className="w-full max-w-md">
                        <audio src={preview} controls className="w-full" />
                      </div>
                    )
                  ) : (
                    <>
                      <Upload className="w-8 h-8 text-slate-500" />
                      <p className="text-sm font-medium text-slate-300">Click to upload file</p>
                      <p className="text-xs text-slate-500">
                        {mode === "audio" ? "Supports MP3, WAV, OGG" : "Supports JPG, PNG"}
                      </p>
                    </>
                  )}
                  <input
                    type="file"
                    ref={fileInputRef}
                    className="hidden"
                    accept={mode === "audio" ? "audio/*" : "image/*"}
                    onChange={handleFileSelect}
                  />
                </div>
                
                {file && (
                  <p className="text-xs text-slate-400 text-center">
                    Selected: <span className="text-slate-200">{file.name}</span>
                  </p>
                )}
              </>
            )}

            <button 
              className="btn-primary mt-2 justify-center py-3"
              onClick={handleAnalyze}
              disabled={loading || (mode === "text" ? !text : !file)}
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  Analyze {mode === "text" ? "Message" : mode === "audio" ? "Voice Note" : "Currency"}
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Column */}
        <div className="flex flex-col gap-4">
          <h2 className="text-lg font-bold text-slate-200">Analysis Result</h2>
          
          {loading ? (
            <div className="glass-card p-12 flex flex-col items-center justify-center gap-4 animate-pulse">
              <div className="w-12 h-12 border-4 border-base-400 border-t-accent-blue rounded-full animate-spin" />
              <p className="text-slate-400 font-medium">Running multi-modal analysis...</p>
            </div>
          ) : result ? (
            <VerdictCard result={result} />
          ) : (
            <div className="glass-card p-12 flex flex-col items-center justify-center gap-3 text-center border-dashed border-base-400">
              <ShieldAlert className="w-10 h-10 text-slate-600 mb-2" />
              <p className="text-slate-400 font-medium text-lg">No analysis yet</p>
              <p className="text-sm text-slate-500 max-w-sm">
                Submit content using the panel on the left to see the AI's verdict and recommended actions.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
