import React, { useMemo } from 'react';
import ReactFlow, { Background, Controls, MarkerType } from 'reactflow';
import dagre from 'dagre';
import 'reactflow/dist/style.css';

// Helper to calculate automatic branching layout
const getLayoutedElements = (nodes, edges) => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({ rankdir: 'TB', nodesep: 100, ranksep: 100 });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: 170, height: 100 });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  return nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - 85,
        y: nodeWithPosition.y - 50,
      },
    };
  });
};

export default function CallGraph({ data }) {
  if (!data || !data.nodes || data.nodes.length === 0) return null;

  const { layoutedNodes, layoutedEdges } = useMemo(() => {
    const nodes = getLayoutedElements(data.nodes, data.edges);
    const edges = data.edges.map((edge) => ({
      ...edge,
      type: 'smoothstep',
      label: edge.label,
      labelStyle: { fill: '#fff', fontWeight: 700 },
      labelBgStyle: { fill: '#1e293b', fillOpacity: 0.8 },
      markerEnd: { type: MarkerType.ArrowClosed, color: '#64748b' },
      style: { stroke: '#64748b', strokeWidth: 2 },
    }));
    return { layoutedNodes: nodes, layoutedEdges: edges };
  }, [data]);

  return (
    <div style={{ width: '100%', height: '600px', background: '#020617' }}>
      <ReactFlow 
        nodes={layoutedNodes} 
        edges={layoutedEdges} 
        fitView
      >
        <Background color="#1e293b" gap={20} />
        <Controls />
      </ReactFlow>
    </div>
  );
}