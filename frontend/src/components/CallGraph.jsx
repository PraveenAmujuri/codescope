import React from "react";
import ReactFlow from "reactflow";
import "reactflow/dist/style.css";

export default function CallGraph({ graph }) {

  if (!graph || graph.length === 0) return null;

  const nodes = [];
  const edges = [];

  const nodeSet = new Set();

  graph.forEach((edge, i) => {

    if (!nodeSet.has(edge.source)) {
      nodes.push({
        id: edge.source,
        data: { label: edge.source },
        position: { x: Math.random() * 400, y: Math.random() * 400 }
      });
      nodeSet.add(edge.source);
    }

    if (!nodeSet.has(edge.target)) {
      nodes.push({
        id: edge.target,
        data: { label: edge.target },
        position: { x: Math.random() * 400, y: Math.random() * 400 }
      });
      nodeSet.add(edge.target);
    }

    edges.push({
      id: `e${i}`,
      source: edge.source,
      target: edge.target
    });

  });

  return (
    <div style={{ height: 400 }}>
      <ReactFlow nodes={nodes} edges={edges} fitView />
    </div>
  );
}