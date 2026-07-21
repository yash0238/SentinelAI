"use client";

import { useEffect, useState } from "react";
import ReportsTable from "@/components/ReportsTable";
import { getReports } from "@/lib/api";

export default function ReportsPage() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const data = await getReports();
      setReports(data);
      setLoading(false);
    }
    load();
  }, []);

  return (
    <div className="h-full flex flex-col space-y-6 animate-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <span className="text-2xl">📋</span> Fraud Reports
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Search and filter all logged incident reports from citizens.
        </p>
      </div>

      {/* Table Area */}
      <div className="flex-1 min-h-[500px]">
        {loading ? (
          <div className="w-full h-full flex items-center justify-center bg-base-800 rounded-xl border border-base-400">
            <div className="spinner" />
          </div>
        ) : (
          <ReportsTable reports={reports} />
        )}
      </div>
    </div>
  );
}
