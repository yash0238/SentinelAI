"use client";

import { useEffect, useRef, useState } from "react";
import { NODE_COLORS } from "@/lib/mock-data";

/**
 * NetworkGraph — A lightweight HTML5 canvas force-directed graph renderer.
 * Visualizes the fraud ring clusters.
 */
export default function NetworkGraph({ data, onNodeClick }) {
  const canvasRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const nodesRef = useRef([]);
  const edgesRef = useRef([]);
  const animationRef = useRef(null);
  const draggedNodeRef = useRef(null);
  const hoverNodeRef = useRef(null);

  // Initialize nodes and edges
  useEffect(() => {
    if (!data?.nodes || !data?.edges) return;
    
    // Assign random initial positions around center
    const w = dimensions.width;
    const h = dimensions.height;
    
    nodesRef.current = data.nodes.map(n => ({
      ...n,
      x: w / 2 + (Math.random() - 0.5) * 200,
      y: h / 2 + (Math.random() - 0.5) * 200,
      vx: 0,
      vy: 0,
      radius: n.type === "victim" || n.type === "suspect" ? 24 : 16,
    }));
    
    edgesRef.current = data.edges.map(e => ({
      ...e,
      sourceObj: nodesRef.current.find(n => n.id === e.source),
      targetObj: nodesRef.current.find(n => n.id === e.target),
    })).filter(e => e.sourceObj && e.targetObj);
    
  }, [data, dimensions.width, dimensions.height]);

  // Handle canvas resize
  useEffect(() => {
    const handleResize = () => {
      if (canvasRef.current) {
        const parent = canvasRef.current.parentElement;
        setDimensions({
          width: parent.clientWidth,
          height: parent.clientHeight
        });
      }
    };
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // Force simulation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!ctx) return;

    const w = dimensions.width;
    const h = dimensions.height;
    
    const tick = () => {
      // 1. Calculate forces
      const nodes = nodesRef.current;
      const edges = edgesRef.current;
      
      // Repulsion (Coulomb)
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[j].x - nodes[i].x;
          const dy = nodes[j].y - nodes[i].y;
          const dist2 = dx * dx + dy * dy;
          if (dist2 === 0) continue;
          
          const dist = Math.sqrt(dist2);
          const force = 4000 / dist2; // Repulsion strength
          const fx = (dx / dist) * force;
          const fy = (dy / dist) * force;
          
          nodes[i].vx -= fx;
          nodes[i].vy -= fy;
          nodes[j].vx += fx;
          nodes[j].vy += fy;
        }
      }
      
      // Attraction (Hooke / Springs)
      for (const edge of edges) {
        const s = edge.sourceObj;
        const t = edge.targetObj;
        const dx = t.x - s.x;
        const dy = t.y - s.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        const targetDist = 120;
        const force = (dist - targetDist) * 0.05; // Spring stiffness
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;
        
        s.vx += fx;
        s.vy += fy;
        t.vx -= fx;
        t.vy -= fy;
      }
      
      // Center gravity
      for (const node of nodes) {
        const dx = w / 2 - node.x;
        const dy = h / 2 - node.y;
        node.vx += dx * 0.01;
        node.vy += dy * 0.01;
      }
      
      // Apply velocity and damping
      for (const node of nodes) {
        if (draggedNodeRef.current === node) continue; // Don't move dragged node
        node.vx *= 0.6; // Damping
        node.vy *= 0.6;
        node.x += node.vx;
        node.y += node.vy;
        
        // Keep in bounds
        node.x = Math.max(node.radius, Math.min(w - node.radius, node.x));
        node.y = Math.max(node.radius, Math.min(h - node.radius, node.y));
      }
      
      // 2. Render
      ctx.clearRect(0, 0, w, h);
      
      // Draw edges
      for (const edge of edges) {
        const s = edge.sourceObj;
        const t = edge.targetObj;
        
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(t.x, t.y);
        ctx.strokeStyle = "rgba(138, 148, 166, 0.4)";
        ctx.lineWidth = 1.5;
        ctx.stroke();
        
        // Draw edge label
        if (edge.label) {
          const mx = (s.x + t.x) / 2;
          const my = (s.y + t.y) / 2;
          ctx.fillStyle = "rgba(14, 19, 31, 0.8)";
          ctx.fillRect(mx - 30, my - 8, 60, 16);
          ctx.fillStyle = "#8a94a6";
          ctx.font = "9px Inter";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(edge.label, mx, my);
        }
      }
      
      // Draw nodes
      for (const node of nodes) {
        const color = NODE_COLORS[node.type] || "#ccc";
        const isHover = hoverNodeRef.current === node;
        
        // Outer glow
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + (isHover ? 6 : 0), 0, 2 * Math.PI);
        ctx.fillStyle = color + (isHover ? "40" : "15");
        ctx.fill();
        
        // Solid center
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
        
        // Text
        ctx.fillStyle = "#fff";
        ctx.font = `600 ${isHover ? "12px" : "10px"} Inter`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(node.label, node.x, node.y + node.radius + 14);
      }
      
      animationRef.current = requestAnimationFrame(tick);
    };
    
    tick();
    return () => cancelAnimationFrame(animationRef.current);
  }, [dimensions.width, dimensions.height]);

  // Mouse interaction handlers
  const handleMouseMove = (e) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    if (draggedNodeRef.current) {
      draggedNodeRef.current.x = x;
      draggedNodeRef.current.y = y;
      return;
    }
    
    // Find hovered node
    const hovered = nodesRef.current.find(n => {
      const dx = n.x - x;
      const dy = n.y - y;
      return dx * dx + dy * dy < (n.radius + 10) * (n.radius + 10);
    });
    
    if (hovered !== hoverNodeRef.current) {
      hoverNodeRef.current = hovered;
      canvasRef.current.style.cursor = hovered ? "pointer" : "default";
    }
  };

  const handleMouseDown = () => {
    if (hoverNodeRef.current) {
      draggedNodeRef.current = hoverNodeRef.current;
      onNodeClick?.(hoverNodeRef.current);
    }
  };

  const handleMouseUp = () => {
    draggedNodeRef.current = null;
  };

  return (
    <div className="w-full h-full relative bg-base-900 rounded-xl overflow-hidden border border-base-400">
      <canvas
        ref={canvasRef}
        width={dimensions.width}
        height={dimensions.height}
        onMouseMove={handleMouseMove}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        className="w-full h-full"
      />
      
      {/* Overlay legend */}
      <div className="absolute top-4 left-4 glass-card px-3 py-2 border border-base-400/50">
        <p className="text-[0.65rem] font-bold text-slate-400 uppercase tracking-wider mb-2">Entity Types</p>
        <div className="grid grid-cols-2 gap-x-4 gap-y-1.5">
          {Object.entries(NODE_COLORS).map(([type, color]) => (
            <div key={type} className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full shadow-[0_0_8px_currentColor]" style={{ color, backgroundColor: color }} />
              <span className="text-xs text-slate-300 capitalize">{type}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
