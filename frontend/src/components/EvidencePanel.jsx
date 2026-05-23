const EvidencePanel = ({ evidence }) => {
  if (!evidence || evidence.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div className="bg-slate-900 px-6 py-4">
        <h2 className="text-white font-bold flex items-center">
          <svg className="w-5 h-5 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          Evidence Audit Trail
        </h2>
      </div>
      <div className="p-6 space-y-4 max-h-[600px] overflow-y-auto">
        {evidence.map((ev, idx) => (
          <div key={idx} className="border-b border-slate-50 last:border-0 pb-4 last:pb-0">
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center">
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase mr-2 ${
                  ev.verdict === 'Supported' ? 'bg-green-100 text-green-700' : 
                  ev.verdict === 'Contradicted' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {ev.verdict}
                </span>
                <span className="text-sm font-bold text-slate-800">{ev.source}</span>
              </div>
              {ev.url && (
                <a href={ev.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline text-xs">
                  View Source
                </a>
              )}
            </div>
            <p className="text-sm text-slate-600 leading-relaxed italic">"{ev.text}"</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EvidencePanel;
