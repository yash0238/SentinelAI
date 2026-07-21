"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Network,
  FileText,
  FlaskConical,
  Shield,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { useState } from "react";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/demo", label: "Live Demo", icon: FlaskConical },
  { href: "/network", label: "Network", icon: Network },
  { href: "/reports", label: "Reports", icon: FileText },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`fixed top-0 left-0 h-screen z-40 flex flex-col border-r border-base-400 bg-base-800/95 backdrop-blur-lg transition-all duration-300 ${
        collapsed ? "w-[68px]" : "w-[230px]"
      }`}
    >
      {/* Brand */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-base-400">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent-blue to-accent-purple flex items-center justify-center flex-shrink-0">
          <Shield className="w-5 h-5 text-white" />
        </div>
        {!collapsed && (
          <div className="overflow-hidden">
            <h1 className="text-[0.95rem] font-extrabold tracking-tight text-slate-100 leading-tight">
              SentinelAI
            </h1>
            <p className="text-[0.6rem] text-slate-500 leading-tight truncate">
              Digital Public Safety
            </p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
          const isActive =
            href === "/" ? pathname === "/" : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={`nav-item relative ${isActive ? "active" : ""}`}
              title={collapsed ? label : undefined}
            >
              <Icon className="w-[18px] h-[18px] flex-shrink-0" />
              {!collapsed && <span>{label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Status */}
      {!collapsed && (
        <div className="px-4 py-3 border-t border-base-400">
          <div className="flex items-center gap-2 text-[0.7rem] text-slate-500">
            <span className="w-2 h-2 rounded-full bg-accent-green animate-pulse" />
            Demo Mode — Mock Data
          </div>
          <p className="text-[0.6rem] text-slate-500 mt-1 leading-relaxed">
            Prototype for demonstration only. Verdicts are advisory.
          </p>
        </div>
      )}

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="mx-3 mb-3 p-2 rounded-lg hover:bg-base-500/40 text-slate-500 transition-colors"
        aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        {collapsed ? (
          <ChevronRight className="w-4 h-4" />
        ) : (
          <ChevronLeft className="w-4 h-4" />
        )}
      </button>
    </aside>
  );
}
