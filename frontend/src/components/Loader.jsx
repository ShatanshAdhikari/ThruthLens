import { useState, useEffect } from 'react';

const STAGES = [
  { label: 'Deconstructing claims', detail: 'LLM extracting atomic facts...' },
  { label: 'Generating search queries', detail: 'Building multi-perspective queries...' },
  { label: 'Harvesting evidence', detail: 'Searching Tavily, Google Fact Check, DuckDuckGo...' },
  { label: 'Running NLI verification', detail: 'DeBERTa cross-encoder scoring each source...' },
  { label: 'Judge Agent synthesizing', detail: 'Weighing source authority and resolving contradictions...' },
  { label: 'Computing risk scores', detail: 'Finalizing consensus analysis...' },
];

const Loader = () => {
  const [stageIndex, setStageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStageIndex(prev => (prev < STAGES.length - 1 ? prev + 1 : prev));
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col p-8 bg-white rounded-xl shadow-md border border-gray-100">
      <div className="flex items-center mb-6">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600 mr-4 flex-shrink-0"></div>
        <div>
          <p className="text-slate-900 font-semibold">{STAGES[stageIndex].label}</p>
          <p className="text-xs text-gray-400 mt-0.5">{STAGES[stageIndex].detail}</p>
        </div>
      </div>
      <div className="space-y-2">
        {STAGES.map((stage, idx) => (
          <div key={idx} className="flex items-center gap-3">
            <span className={`w-2 h-2 rounded-full flex-shrink-0 ${
              idx < stageIndex ? 'bg-green-500' : idx === stageIndex ? 'bg-blue-500 animate-pulse' : 'bg-gray-200'
            }`} />
            <span className={`text-xs ${idx < stageIndex ? 'text-green-600 font-medium' : idx === stageIndex ? 'text-slate-700 font-semibold' : 'text-gray-400'}`}>
              {stage.label}
            </span>
            {idx < stageIndex && (
              <svg className="w-3 h-3 text-green-500 ml-auto flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Loader;
