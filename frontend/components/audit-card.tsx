'use client';

import { ArrowRight } from 'lucide-react';
import { Badge } from './ui/badge';
import { Card } from './ui/card';

export interface AuditCardData {
  id: string;
  title: string;
  summary: string;
  severity: 'red' | 'yellow' | 'green';
  library: string;
  deprecated: boolean;
  migrationPath: string | null;
  coordinates: {
    page: number;
    top: number;
    left: number;
    width: number;
    height: number;
    label: string;
  };
}

interface AuditCardProps {
  card: AuditCardData;
  selected: boolean;
  onClick: (card: AuditCardData) => void;
}

export function AuditCard({ card, selected, onClick }: AuditCardProps) {
  return (
    <Card
      className={`cursor-pointer border transition duration-200 ${
        selected ? 'border-sky-400 bg-slate-800/95 shadow-[0_20px_50px_-30px_rgba(56,189,248,0.75)]' : 'border-slate-800 bg-slate-950/80 hover:border-slate-500'
      }`}
      onClick={() => onClick(card)}
    >
      <div className="space-y-4 p-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-400">{card.library}</p>
            <h3 className="mt-2 text-lg font-semibold text-white">{card.title}</h3>
          </div>
          <Badge variant={card.deprecated ? 'default' : 'secondary'}>
            {card.deprecated ? 'Deprecated' : 'Safe'}
          </Badge>
        </div>

        <p className="text-sm leading-6 text-slate-300">{card.summary}</p>

        {card.migrationPath ? (
          <div className="rounded-2xl bg-slate-950/90 p-4 text-sm text-slate-300">
            <p className="font-semibold text-slate-100">Migration Path</p>
            <p className="mt-2 text-slate-400">{card.migrationPath}</p>
          </div>
        ) : null}

        <div className="flex items-center justify-between gap-3 pt-3 text-sm text-slate-400">
          <span>Page {card.coordinates.page}</span>
          <div className="flex items-center gap-2 text-sky-300">
            <span>View evidence</span>
            <ArrowRight className="h-4 w-4" />
          </div>
        </div>
      </div>
    </Card>
  );
}
