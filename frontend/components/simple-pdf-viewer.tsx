'use client';

import { useEffect, useRef, useState } from 'react';

interface SimplePdfViewerProps {
  pdfUrl?: string;
  highlightLocation?: string | null;
}

export function SimplePdfViewer({ pdfUrl = '/testdoc.pdf', highlightLocation }: SimplePdfViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    if (highlightLocation && iframeRef.current) {
      // Implement basic page navigation based on claim ID
      // Extract claim index from ID (e.g., "claim-0" -> index 0, "claim-5" -> index 5)
      const claimMatch = highlightLocation.match(/claim-(\d+)/);
      if (claimMatch) {
        const claimIndex = parseInt(claimMatch[1]);

        // Rough estimation: distribute claims across pages
        // For LoRA paper (26 pages), distribute claims roughly evenly
        const estimatedPage = Math.min(Math.floor((claimIndex / 10) * 26) + 1, 26);

        // Navigate to specific page in PDF with highlight
        iframeRef.current.src = `${pdfUrl}#page=${estimatedPage}&toolbar=0&navpanes=0&search=${encodeURIComponent(highlightLocation)}`;
        setCurrentPage(estimatedPage);
      }
    }
  }, [highlightLocation, pdfUrl]);

  return (
    <div
      ref={containerRef}
      className="relative h-full w-full overflow-auto rounded-2xl border border-slate-700 bg-slate-950"
    >
      <iframe
        ref={iframeRef}
        src={`${pdfUrl}#toolbar=0&navpanes=0`}
        className="h-full w-full"
        title="PDF Viewer"
        style={{ border: 'none', borderRadius: '1rem' }}
      />

      {/* Highlight overlay */}
      {highlightLocation && (
        <div className="pointer-events-none absolute top-4 right-4 rounded-lg bg-red-500/90 px-4 py-2 text-sm text-white border border-red-400 shadow-lg animate-pulse">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-red-300 rounded-full animate-ping"></div>
            Highlighted: {highlightLocation} (Page {currentPage})
          </div>
        </div>
      )}
    </div>
  );
}
