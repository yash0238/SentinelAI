"use client";

import { useEffect, useState } from "react";
import StatCard from "@/components/StatCard";
import HotspotMap from "@/components/HotspotMap";
import { getStats, getHotspots, getScamTrend, getScamTypeBreakdown } from "@/lib/api";
import { Activity, ShieldAlert, FileText, BadgeAlert, IndianRupee, Zap } from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from "recharts";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [hotspots, setHotspots] = useState(null);
  const [trend, setTrend] = useState([]);
  const [breakdown, setBreakdown] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [s, h, t, b] = await Promise.all([
        getStats(),
        getHotspots(),
        getScamTrend(),
        getScamTypeBreakdown(),
      ]);
      setStats(s);
      setHotspots(h);
      setTrend(t);
      // Sort breakdown by count ascending for horizontal bar chart
      setBreakdown(b.sort((x, y) => x.count - y.count));
      setLoading(false);
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="spinner" />
      </div>
    );
  }

  const statCards = [
    { label: "Active sessions", val: stats?.active_sessions, icon: Activity, color: "#ff7f0e" },
    { label: "High-risk today", val: stats?.high_risk_today, icon: ShieldAlert, color: "#ff2e63" },
    { label: "Total reports", val: stats?.total_reports?.toLocaleString(), icon: FileText, color: "#4da6ff" },
    { label: "Counterfeit flags", val: stats?.counterfeit_flags, icon: BadgeAlert, color: "#a66bff" },
    { label: "Fraud blocked", val: `₹${stats?.amount_saved_cr} Cr`, icon: IndianRupee, color: "#2ecc71" },
    { label: "Avg. detection", val: `${stats?.avg_detection_seconds}s`, icon: Zap, color: "#00d0d0" },
  ];

  return (
    <div className="space-y-6 animate-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Command Overview</h1>
        <p className="text-sm text-slate-400 mt-1">Live metrics across all intelligence channels.</p>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {statCards.map((c, i) => (
          <StatCard
            key={c.label}
            label={c.label}
            value={c.val}
            icon={c.icon}
            accent={c.color}
            delay={i + 1}
          />
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[500px]">
        
        {/* Map (Spans 7 cols) */}
        <div className="lg:col-span-7 h-full flex flex-col gap-3">
          <h2 className="text-[0.95rem] font-bold text-slate-200 flex items-center gap-2">
            <span className="text-xl">🗺️</span> Active Digital-Arrest Hotspots
          </h2>
          <div className="flex-1 rounded-xl shadow-card relative">
            <HotspotMap hotspots={hotspots} />
          </div>
        </div>

        {/* Charts (Spans 5 cols) */}
        <div className="lg:col-span-5 h-full flex flex-col gap-6">
          
          {/* Trend Chart */}
          <div className="flex-1 flex flex-col gap-3">
            <h2 className="text-[0.95rem] font-bold text-slate-200 flex items-center gap-2">
              <span className="text-xl">📈</span> Reports (14 days)
            </h2>
            <div className="flex-1 bg-base-800 rounded-xl border border-base-400 p-4">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trend} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorReports" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#4da6ff" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#4da6ff" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="date" stroke="#6b7588" fontSize={11} tickLine={false} axisLine={false} />
                  <YAxis stroke="#6b7588" fontSize={11} tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0e131f', border: '1px solid #232c42', borderRadius: '8px' }}
                    itemStyle={{ color: '#c7d0e0' }}
                  />
                  <Area type="monotone" dataKey="reports" stroke="#4da6ff" strokeWidth={2} fillOpacity={1} fill="url(#colorReports)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Breakdown Chart */}
          <div className="flex-1 flex flex-col gap-3">
            <h2 className="text-[0.95rem] font-bold text-slate-200 flex items-center gap-2">
              <span className="text-xl">🧬</span> Scam Type Breakdown
            </h2>
            <div className="flex-1 bg-base-800 rounded-xl border border-base-400 p-4 pl-0">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={breakdown} layout="vertical" margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="scam_type" type="category" stroke="#a0aec0" fontSize={10} tickLine={false} axisLine={false} width={130} />
                  <Tooltip 
                    cursor={{fill: 'rgba(77,166,255,0.05)'}}
                    contentStyle={{ backgroundColor: '#0e131f', border: '1px solid #232c42', borderRadius: '8px' }}
                  />
                  <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                    {breakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={`hsl(260, 70%, ${50 + (index * 35) / breakdown.length}%)`} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
