'use client';

import { useEffect, useRef } from 'react';

interface HighlightProps {
  page: number;
  top: number;
  left: number;
  width: number;
  height: number;
  label?: string;
}

interface PdfViewerProps {
  selectedHighlight?: HighlightProps | null;
  selectedLabel?: string | null;
  pdfLines?: string[];
}

const fakePageLines = [
  '1. Import pdfminer.six for PDF extraction and parse each page into text blocks.',
  '2. Use requests.get to fetch external metadata for referenced project dependencies.',
  '3. Run a static audit across extracted content looking for deprecated packages in the dependency graph.',
  '4. Flag outdated libraries that require migration to the 2026 compatibility layer.',
  '5. Generate a report with exact evidence coordinates and migration recommendations.',
  '6. Ensure the PDF highlights appear instantly when an audit card is selected.',
  '7. The audit should be able to correlate claims with page-level evidence inside the document.',
  '8. This viewer demonstrates a proof-of-concept highlight overlay for PDF evidence.',
];

export function PdfViewer({ selectedHighlight, selectedLabel, pdfLines }: PdfViewerProps) {
  const pageRef = useRef<HTMLDivElement | null>(null);

  const pageLines = pdfLines && pdfLines.length > 0 ? pdfLines : fakePageLines;

  useEffect(() => {
    if (!selectedHighlight || !pageRef.current) {
      return;
    }

    const highlightElement = pageRef.current.querySelector(`[data-highlight-id="${selectedHighlight.label}"]`) as HTMLElement | null;
    highlightElement?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [selectedHighlight]);

  return (
    <div className="rounded-[2rem] border border-slate-800 bg-slate-900/95 p-6 shadow-[0_40px_120px_-80px_rgba(15,23,42,0.7)]">
      <div className="mb-6 flex items-center justify-between gap-3">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">PDF Viewer</p>
          <h2 className="text-2xl font-semibold text-white">Evidence preview</h2>
        </div>
        <div className="rounded-full bg-slate-950 px-4 py-2 text-sm text-slate-300">
          Page 1 of 1
        </div>
      </div>

      <div className="relative overflow-hidden rounded-[1.75rem] border border-slate-800 bg-slate-950/95 p-6 shadow-inner shadow-slate-950/20">
        <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-sky-500/10 to-transparent" />
        <div className="relative h-[540px] overflow-y-auto rounded-[1.5rem] border border-slate-800 bg-slate-900 p-6" ref={pageRef}>
          <div className="space-y-5">
            {pageLines.map((line, index) => {
              const isHighlighted = selectedHighlight?.label === `evidence-${index}`;
              return (
                <div
                  key={index}
                  data-highlight-id={`evidence-${index}`}
                  className={`relative overflow-hidden rounded-3xl border border-slate-800/90 p-5 text-sm leading-7 text-slate-200 ${
                    isHighlighted ? 'border-sky-400/50 bg-sky-500/10 shadow-[0_0_0_1px_rgba(56,189,248,0.25)]' : 'bg-slate-950/80'
                  }`}
                >
                  <span className="block text-slate-400">Line {index + 1}</span>
                  <p>{line}</p>
                </div>
              );
            })}
          </div>

          {selectedHighlight ? (
            <div
              className="pointer-events-none absolute rounded-3xl border border-sky-400/60 bg-sky-400/10 transition-all duration-300"
              style={{
                top: `${selectedHighlight.top}%`,
                left: `${selectedHighlight.left}%`,
                width: `${selectedHighlight.width}%`,
                height: `${selectedHighlight.height}%`,
              }}
            />
          ) : null}
        </div>
      </div>

      <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/90 p-4 text-sm text-slate-300">
        <p className="text-slate-400">Selected evidence</p>
        <p className="mt-2 text-white">{selectedLabel ?? 'Select a red audit card to highlight the supporting PDF text.'}</p>
      </div>
    </div>
  );
}
