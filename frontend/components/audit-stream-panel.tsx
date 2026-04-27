'use client';

interface Claim {
  text: string;
  id: string;
}

interface FindingsData {
  claims: Claim[];
  deprecated: Claim[];
  searchResults: any[]; // Can be string or object with url/content
  auditReport: string;
}

interface AuditStreamPanelProps {
  findings: FindingsData;
  onClaimClick: (claimId: string) => void;
  selectedClaimId: string | null;
}

export function AuditStreamPanel({ findings, onClaimClick, selectedClaimId }: AuditStreamPanelProps) {
  return (
    <div className="space-y-6 text-slate-200 overflow-y-auto">
      {/* Finding Claims */}
      <div>
        <h2 className="text-base font-normal text-white mb-3">finding claims.....</h2>
        <div className="space-y-2 pl-4">
          {findings.claims.length === 0 ? (
            <p className="text-sm text-slate-500 italic">No claims found yet...</p>
          ) : (
            findings.claims.map((claim) => (
              <div key={claim.id} className="text-sm text-slate-300">
                • {claim.text}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Outdated Dependencies */}
      <div>
        <h2 className="text-base font-normal text-white mb-3">finding outdated dependencies.....</h2>
        <div className="space-y-2 pl-4">
          {findings.deprecated.length === 0 ? (
            <p className="text-sm text-slate-500 italic">No deprecated dependencies found...</p>
          ) : (
            findings.deprecated.map((dep) => (
              <button
                key={dep.id}
                onClick={() => onClaimClick(dep.id)}
                className={`block text-left text-sm transition ${
                  selectedClaimId === dep.id ? 'text-red-300 font-semibold' : 'text-slate-300 hover:text-slate-100'
                }`}
              >
                • {dep.text}
              </button>
            ))
          )}
        </div>
      </div>

      {/* Search Results */}
      {findings.searchResults.length > 0 && (
        <div>
          <h2 className="text-base font-normal text-white mb-3">search references.....</h2>
          <div className="space-y-3 pl-4">
            {findings.searchResults.map((result, idx) => {
              const isObject = typeof result === 'object' && result.url;
              const url = isObject ? result.url : '';
              const content = isObject ? result.content : result;
              
              return (
                <div key={idx} className="text-xs text-slate-400 leading-relaxed">
                  {url ? (
                    <a 
                      href={url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:text-blue-300 underline"
                    >
                      {content}
                    </a>
                  ) : (
                    <span>{content}</span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Audit Report */}
      {findings.auditReport && (
        <div>
          <h2 className="text-base font-normal text-white mb-3">audit report.....</h2>
          <div className="bg-slate-900/50 border border-slate-700 rounded p-4 text-xs text-slate-300 leading-relaxed whitespace-pre-wrap max-h-80 overflow-auto">
            {findings.auditReport}
          </div>
        </div>
      )}
    </div>
  );
}
