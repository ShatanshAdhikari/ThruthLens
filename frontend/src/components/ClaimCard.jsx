import { useState } from 'react';

const ClaimCard = ({ data }) => {
  const [showAllEvidence, setShowAllEvidence] = useState(false);
  const {
    claim, status, risk_score, confidence, consensus_stats,
    explanation, reasoning, evidence_details
  } = data;

  const getStatusColor = () => {
    switch (status) {
      case 'Supported': return 'bg-green-100 text-green-800 border-green-200';
      case 'Contradicted': return 'bg-red-100 text-red-800 border-red-200';
      case 'Insufficient Evidence': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getVerdictBadge = (verdict) => {
    switch (verdict) {
      case 'Supported': return 'text-green-600';
      case 'Contradicted': return 'text-red-600';
      default: return 'text-yellow-600';
    }
  };

  return (
    <div className={`p-6 rounded-xl border shadow-sm bg-white transition-all hover:shadow-md mb-6`}>
      <div className="flex justify-between items-start mb-4">
        <h3 className="font-bold text-xl text-slate-900 leading-tight pr-4">{claim}</h3>
        <span className={`px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest border-2 ${getStatusColor()}`}>
          {status}
        </span>
      </div>
      
      {/* Consensus Bar */}
      {consensus_stats && (
        <div className="mb-6">
          <div className="flex justify-between text-[10px] font-bold uppercase text-gray-400 mb-1.5 px-1">
            <span>Evidence Consensus</span>
            <span>{evidence_details?.length || 0} Sources Analyzed</span>
          </div>
          <div className="h-3 w-full bg-gray-100 rounded-full flex overflow-hidden border border-gray-100 shadow-inner">
            <div 
              className="h-full bg-green-500 transition-all duration-500" 
              style={{ width: `${(consensus_stats.Supported / (evidence_details?.length || 1)) * 100}%` }}
              title={`Supported by ${consensus_stats.Supported} sources`}
            ></div>
            <div 
              className="h-full bg-red-500 transition-all duration-500" 
              style={{ width: `${(consensus_stats.Contradicted / (evidence_details?.length || 1)) * 100}%` }}
              title={`Contradicted by ${consensus_stats.Contradicted} sources`}
            ></div>
            <div 
              className="h-full bg-yellow-400 transition-all duration-500" 
              style={{ width: `${(consensus_stats['Insufficient Evidence'] / (evidence_details?.length || 1)) * 100}%` }}
              title={`${consensus_stats['Insufficient Evidence']} sources provided insufficient evidence`}
            ></div>
          </div>
        </div>
      )}

      {reasoning && (
        <div className="mb-6 bg-slate-900 p-5 rounded-xl border border-slate-800 shadow-lg">
          <div className="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-2 flex items-center">
            <svg className="w-3 h-3 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
            Clinical Audit Reasoning
          </div>
          <p className="text-sm text-slate-300 leading-relaxed font-medium italic">
            {reasoning}
          </p>
        </div>
      )}

      {explanation && (
        <div className="mb-6 bg-blue-50/50 p-4 rounded-xl border border-blue-100/50">
          <div className="text-[10px] font-black text-blue-500 uppercase tracking-widest mb-2">Brief Explanation</div>
          <p className="text-sm text-slate-700 leading-relaxed font-medium">{explanation}</p>
        </div>
      )}

      {/* Multi-Source Evidence List */}
      <div className="space-y-3">
        <div className="text-[10px] font-black text-gray-400 uppercase tracking-widest px-1">Primary Evidence Sources</div>
        {(showAllEvidence ? evidence_details : evidence_details?.slice(0, 3))?.map((ev, idx) => (
          <div key={idx} className="bg-slate-50 p-4 rounded-xl border border-slate-100 hover:border-blue-200 transition-colors">
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center">
                <span className={`w-2 h-2 rounded-full mr-2 ${
                  ev.verdict === 'Supported' ? 'bg-green-500' : ev.verdict === 'Contradicted' ? 'bg-red-500' : 'bg-yellow-500'
                }`}></span>
                <span className="text-[11px] font-bold text-slate-500 uppercase truncate max-w-[120px]">
                  {ev.source}
                </span>
                {ev.relevance_score != null && (
                  <span className={`ml-1 text-[9px] font-bold px-1 rounded ${
                    ev.relevance_score >= 0.5 ? 'bg-blue-50 text-blue-500' :
                    ev.relevance_score >= 0.3 ? 'bg-slate-100 text-slate-400' : 'bg-orange-50 text-orange-400'
                  }`}>
                    {(ev.relevance_score * 100).toFixed(0)}%
                  </span>
                )}
                {ev.url && (
                  <a href={ev.url} target="_blank" rel="noopener noreferrer" className="ml-2 text-blue-400 hover:text-blue-600">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                )}
              </div>
              <span className={`text-[10px] font-black uppercase ${getVerdictBadge(ev.verdict)}`}>
                {ev.verdict}
              </span>
            </div>
            <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed italic">"{ev.text}"</p>
          </div>
        ))}
        {evidence_details?.length > 3 && (
          <button
            onClick={() => setShowAllEvidence(prev => !prev)}
            className="w-full text-xs font-bold text-blue-500 hover:text-blue-700 py-2 border border-dashed border-blue-200 rounded-lg hover:bg-blue-50 transition-colors"
          >
            {showAllEvidence
              ? 'Show fewer sources'
              : `Show ${evidence_details.length - 3} more source${evidence_details.length - 3 > 1 ? 's' : ''}`}
          </button>
        )}
      </div>
      
      <div className="mt-6 flex gap-6 items-center border-t pt-5 border-slate-100">
        <div className="flex flex-col">
          <div className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Hallucination Risk</div>
          <div className="flex items-center gap-2">
            <div className="w-20 bg-gray-100 rounded-full h-2 shadow-inner">
              <div 
                className={`h-2 rounded-full ${risk_score > 0.7 ? 'bg-red-500' : risk_score > 0.3 ? 'bg-yellow-500' : 'bg-green-500'}`}
                style={{ width: `${risk_score * 100}%` }}
              ></div>
            </div>
            <span className="text-xs font-black text-slate-700">{(risk_score * 100).toFixed(0)}%</span>
          </div>
        </div>

        <div className="flex flex-col border-l pl-6 border-slate-100">
          <div className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Model Confidence</div>
          <div className="flex items-center gap-2">
            <div className="w-20 bg-gray-100 rounded-full h-2 shadow-inner">
              <div 
                className="h-2 rounded-full bg-blue-500"
                style={{ width: `${confidence * 100}%` }}
              ></div>
            </div>
            <span className="text-xs font-black text-slate-700">{(confidence * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClaimCard;
