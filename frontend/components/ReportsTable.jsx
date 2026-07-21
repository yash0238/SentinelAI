"use client";

import { useState } from "react";
import { RISK_COLORS } from "@/lib/mock-data";
import { Search, Filter, ChevronLeft, ChevronRight } from "lucide-react";

/**
 * ReportsTable — Sortable, filterable table of fraud reports.
 */
export default function ReportsTable({ reports = [] }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [riskFilter, setRiskFilter] = useState("ALL");
  const [page, setPage] = useState(1);
  const itemsPerPage = 10;

  // Filter
  const filtered = reports.filter((r) => {
    const matchesSearch =
      r.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.scam_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.city.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRisk = riskFilter === "ALL" || r.risk_level === riskFilter;
    return matchesSearch && matchesRisk;
  });

  // Pagination
  const totalPages = Math.ceil(filtered.length / itemsPerPage);
  const paginated = filtered.slice(
    (page - 1) * itemsPerPage,
    page * itemsPerPage
  );

  return (
    <div className="flex flex-col h-full">
      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center mb-6">
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search reports by ID, type, city..."
            className="input-field pl-9"
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setPage(1);
            }}
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-500" />
          <div className="flex bg-base-800 rounded-lg p-1 border border-base-400">
            {["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"].map((level) => (
              <button
                key={level}
                onClick={() => {
                  setRiskFilter(level);
                  setPage(1);
                }}
                className={`px-3 py-1 text-xs font-semibold rounded-md transition-colors ${
                  riskFilter === level
                    ? "bg-base-600 text-slate-100 shadow-sm"
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="flex-1 bg-base-800 rounded-xl border border-base-400 overflow-hidden flex flex-col">
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Time</th>
                <th>Scam Type</th>
                <th>Risk</th>
                <th>Score</th>
                <th>City</th>
                <th>Amount (₹)</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {paginated.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-8 text-slate-500">
                    No reports found matching your criteria.
                  </td>
                </tr>
              ) : (
                paginated.map((r) => (
                  <tr key={r.id} className="cursor-pointer">
                    <td className="font-mono text-xs">{r.id}</td>
                    <td className="text-slate-400 whitespace-nowrap">
                      {r.created_at}
                    </td>
                    <td className="font-medium text-slate-200">{r.scam_type}</td>
                    <td>
                      <span
                        className={`risk-badge risk-${r.risk_level.toLowerCase()}`}
                      >
                        {r.risk_level}
                      </span>
                    </td>
                    <td>
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1.5 bg-base-600 rounded-full overflow-hidden">
                          <div
                            className="h-full rounded-full"
                            style={{
                              width: `${r.risk_score}%`,
                              backgroundColor: RISK_COLORS[r.risk_level],
                            }}
                          />
                        </div>
                        <span className="text-xs font-mono">{r.risk_score}</span>
                      </div>
                    </td>
                    <td>{r.city}</td>
                    <td className="font-mono">
                      {r.amount_involved > 0
                        ? `₹${r.amount_involved.toLocaleString()}`
                        : "-"}
                    </td>
                    <td>
                      <span className="px-2 py-1 bg-base-600 text-slate-300 text-xs rounded border border-base-400">
                        {r.status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination footer */}
        <div className="mt-auto px-4 py-3 border-t border-base-400 bg-base-900 flex items-center justify-between">
          <span className="text-xs text-slate-500">
            Showing {(page - 1) * itemsPerPage + 1} to{" "}
            {Math.min(page * itemsPerPage, filtered.length)} of {filtered.length}{" "}
            reports
          </span>
          <div className="flex gap-1">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-1 rounded bg-base-800 border border-base-400 text-slate-400 disabled:opacity-50"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages || totalPages === 0}
              className="p-1 rounded bg-base-800 border border-base-400 text-slate-400 disabled:opacity-50"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
