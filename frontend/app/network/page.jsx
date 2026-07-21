"use client";

import { useEffect, useState } from "react";
import NetworkGraph from "@/components/NetworkGraph";
import { getClusters } from "@/lib/api";
import { Box, FileWarning, Fingerprint, MapPin, Smartphone, User, Link as LinkIcon, Download, Network } from "lucide-react";
import { NODE_COLORS } from "@/lib/mock-data";

export default function NetworkPage() {
  const [cluster, setCluster] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const data = await getClusters();
      setCluster(data);
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

  const getNodeIcon = (type) => {
    switch (type) {
      case "victim": return User;
      case "suspect": return FileWarning;
      case "phone": return Smartphone;
      case "device": return Fingerprint;
      case "ip": return MapPin;
      case "upi": return Box;
      default: return Box;
    }
  };

  return (
    <div className="h-full flex flex-col space-y-4 animate-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <span className="text-2xl">🕸️</span> Fraud Network Intelligence
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Cluster <strong className="text-slate-200">{cluster?.cluster_id}</strong> — isolated victim reports linked into a single money-mule network.
          </p>
        </div>
        <button 
          className="btn-primary"
          onClick={() => alert(`Generated intelligence package for ${cluster?.cluster_id} with full provenance and audit trail.`)}
        >
          <Download className="w-4 h-4" />
          Generate Intel Package
        </button>
      </div>

      {/* Main Area */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6 min-h-0">
        
        {/* Graph (3/4 width) */}
        <div className="lg:col-span-3 h-full shadow-card rounded-xl">
          <NetworkGraph data={cluster} onNodeClick={setSelectedNode} />
        </div>

        {/* Side Panel (1/4 width) */}
        <div className="lg:col-span-1 flex flex-col gap-4">
          <div className="glass-card flex-1 p-5 flex flex-col">
            <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 border-b border-base-400 pb-2">
              Entity Details
            </h3>
            
            {selectedNode ? (
              <div className="space-y-6 animate-fade-in">
                <div className="flex items-center gap-4">
                  <div 
                    className="w-12 h-12 rounded-xl flex items-center justify-center shadow-lg"
                    style={{ 
                      backgroundColor: `${NODE_COLORS[selectedNode.type]}20`,
                      color: NODE_COLORS[selectedNode.type],
                      border: `1px solid ${NODE_COLORS[selectedNode.type]}40`
                    }}
                  >
                    {(() => {
                      const Icon = getNodeIcon(selectedNode.type);
                      return <Icon className="w-6 h-6" />;
                    })()}
                  </div>
                  <div>
                    <p className="text-lg font-bold text-slate-100 leading-tight">{selectedNode.label}</p>
                    <p className="text-xs font-semibold uppercase tracking-wider" style={{ color: NODE_COLORS[selectedNode.type] }}>
                      {selectedNode.type}
                    </p>
                  </div>
                </div>

                <div className="space-y-3 pt-2">
                  <div className="bg-base-900 rounded-lg p-3 border border-base-400">
                    <p className="text-xs text-slate-500 mb-1">Entity ID</p>
                    <p className="text-sm font-mono text-slate-300">{selectedNode.id}</p>
                  </div>
                  <div className="bg-base-900 rounded-lg p-3 border border-base-400">
                    <p className="text-xs text-slate-500 mb-1">Connections in cluster</p>
                    <p className="text-sm font-mono text-slate-300">
                      {cluster.edges.filter(e => e.source === selectedNode.id || e.target === selectedNode.id).length} links
                    </p>
                  </div>
                </div>

                <div className="pt-4 border-t border-base-400">
                  <p className="text-xs text-slate-500 mb-2">Connected to:</p>
                  <div className="space-y-2">
                    {cluster.edges
                      .filter(e => e.source === selectedNode.id || e.target === selectedNode.id)
                      .map((e, i) => {
                        const isSource = e.source === selectedNode.id;
                        const otherId = isSource ? e.target : e.source;
                        const otherNode = cluster.nodes.find(n => n.id === otherId);
                        return (
                          <div key={i} className="flex items-center gap-2 text-sm bg-base-800/50 p-2 rounded">
                            <LinkIcon className="w-3 h-3 text-slate-500" />
                            <span className="text-slate-400 italic text-xs w-20">{e.label}</span>
                            <span className="text-slate-200 truncate">{otherNode?.label}</span>
                          </div>
                        );
                    })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center opacity-50">
                <Network className="w-12 h-12 text-slate-500 mb-3" />
                <p className="text-slate-400 font-medium">No entity selected</p>
                <p className="text-xs text-slate-500 mt-1 max-w-[200px]">
                  Click on a node in the graph to view its details and connections.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
