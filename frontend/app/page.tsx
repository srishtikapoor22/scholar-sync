'use client';

import { useEffect, useState } from 'react';
import { SimplePdfViewer } from '@/components/simple-pdf-viewer';
import { AuditStreamPanel } from '@/components/audit-stream-panel';

interface Claim {
  text: string;
  id: string;
}

interface Findings {
  claims: Claim[];
  deprecated: Claim[];
  searchResults: any[]; // Can be string or object with url/content
  auditReport: string;
}

export default function HomePage() {
  const [findings, setFindings] = useState<Findings>({
    claims: [],
    deprecated: [],
    searchResults: [],
    auditReport: '',
  });
  const [selectedClaimId, setSelectedClaimId] = useState<string | null>(null);
  const [status, setStatus] = useState('Connecting to audit stream...');

  useEffect(() => {
    const hasReceivedData = { current: false };
    let timeoutId: NodeJS.Timeout;
    const source = new EventSource('/api/audit');

    const resetTimeout = () => {
      if (timeoutId) clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        console.log('Audit stream timeout - assuming complete');
        setStatus('Audit complete!');
        source.close();
      }, 15000); // 15 second timeout
    };

    source.onopen = () => {
      console.log('EventSource connected');
      setStatus('Connected to audit stream...');
      resetTimeout();
    };

    source.onmessage = (event) => {
      console.log('Received message:', event.data);
      hasReceivedData.current = true;
      resetTimeout();
    };

    source.addEventListener('claim', (event) => {
      const payload = JSON.parse((event as MessageEvent).data);
      setFindings((prev) => ({
        ...prev,
        claims: [...prev.claims, payload],
      }));
      setStatus('Finding claims...');
      hasReceivedData.current = true;
      resetTimeout();
    });

    source.addEventListener('deprecated', (event) => {
      const payload = JSON.parse((event as MessageEvent).data);
      setFindings((prev) => ({
        ...prev,
        deprecated: [...prev.deprecated, payload],
      }));
      setStatus('Identifying deprecated dependencies...');
      hasReceivedData.current = true;
      resetTimeout();
    });

    source.addEventListener('status', (event) => {
      const payload = JSON.parse((event as MessageEvent).data);
      setStatus(payload.message);
      hasReceivedData.current = true;
      resetTimeout();
    });

    source.addEventListener('error', (event) => {
      console.error('EventSource error:', event);
      // Only show error if we haven't received any data
      if (!hasReceivedData.current) {
        setStatus('Connection lost to audit stream.');
      } else {
        setStatus('Audit complete!');
      }
      source.close();
      if (timeoutId) clearTimeout(timeoutId);
    });

    source.addEventListener('search', (event) => {
      const payload = JSON.parse((event as MessageEvent).data);
      setFindings((prev) => ({
        ...prev,
        searchResults: [...prev.searchResults, payload.result],
      }));
      setStatus('Searching for current library status...');
      hasReceivedData.current = true;
      resetTimeout();
    });

    source.addEventListener('report', (event) => {
      const payload = JSON.parse((event as MessageEvent).data);
      setFindings((prev) => ({
        ...prev,
        auditReport: payload.report,
      }));
      setStatus('Audit complete!');
      hasReceivedData.current = true;
      source.close();
      if (timeoutId) clearTimeout(timeoutId);
    });

    source.addEventListener('done', () => {
      console.log('Audit stream completed');
      source.close();
      setStatus('Audit complete!');
      hasReceivedData.current = true;
      if (timeoutId) clearTimeout(timeoutId);
    });

    return () => {
      source.close();
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex h-screen flex-col">
        {/* Header */}
        <div className="border-b border-slate-800 bg-slate-900/80 px-8 py-4">
          <div className="mx-auto max-w-7xl">
            <h1 className="text-2xl font-bold text-white">Scholar Sync Audit</h1>
            <p className="mt-1 text-sm text-slate-400">{status}</p>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex flex-1 overflow-hidden">
          {/* Left: PDF Viewer */}
          <div className="w-1/2 border-r border-slate-800 p-6 overflow-hidden">
            <SimplePdfViewer pdfUrl="/testdoc.pdf" highlightLocation={selectedClaimId || undefined} />
          </div>

          {/* Right: Findings Panel */}
          <div className="w-1/2 overflow-y-auto border-l border-slate-800 bg-slate-900/50 p-6">
            <AuditStreamPanel findings={findings} onClaimClick={setSelectedClaimId} selectedClaimId={selectedClaimId} />
          </div>
        </div>
      </div>
    </main>
  );
}

