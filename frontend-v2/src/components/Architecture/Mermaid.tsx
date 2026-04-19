import React from 'react';
import Mermaid from 'beautiful-mermaid';
import { cn } from '../../lib/utils';

interface MermaidCanvasProps {
  chart: string;
  className?: string;
  id?: string;
}

const MermaidCanvas: React.FC<MermaidCanvasProps> = ({ chart, className, id }) => {
  return (
    <div id={id} className={cn('glass border border-white/10 rounded-2xl p-8', className)}>
      <Mermaid 
        chart={chart}
        theme="dark"
        config={{
          themeVariables: {
            primaryColor: 'rgba(34,211,238,0.1)',
            primaryBorderColor: '#22d3ee',
            primaryTextColor: '#f8fafc',
            lineColor: '#64748b',
          }
        }}
      />
    </div>
  );
};

export default MermaidCanvas;
