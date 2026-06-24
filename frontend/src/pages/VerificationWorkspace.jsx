import { useState } from 'react';
import ClaimCard from '../components/ClaimCard';
import Loader from '../components/Loader';
import DashboardChart from '../components/DashboardChart';
import Heatmap from '../components/Heatmap';
import ConfidenceMeter from '../components/ConfidenceMeter';
import EvidencePanel from '../components/EvidencePanel';

const VerificationWorkspace = () => {
  const [text, setText] = useState('');
  const [claims, setClaims] = useState([]);
  const [overallRisk, setOverallRisk] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [totalClaims, setTotalClaims] = useState(null);
  const [totalTimeMs, setTotalTimeMs] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const isComplete = overallRisk !== null;
  const pendingCount = totalClaims !== null ? totalClaims - claims.length : 0;

  const handleVerify = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setClaims([]);
    setOverallRisk(null);
    setJobId(null);
    setTotalClaims(null);
    setTotalTimeMs(null);

    try {
      const response = await fetch('/api/verify/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const event = JSON.parse(line.slice(6));

          if (event.type === 'start') {
            setTotalClaims(event.claim_count);
          } else if (event.type === 'claim') {
            setClaims(prev => [...prev, event.data]);
          } else if (event.type === 'complete') {
            setOverallRisk(event.overall_risk);
            setJobId(event.job_id);
            setTotalTimeMs(event.total_time_ms);
            setLoading(false);
          } else if (event.type === 'error') {
            throw new Error(event.message);
          }
        }
      }
    } catch (err) {
      setError('Failed to verify text. Please ensure the backend is running.');
      console.error(err);
      setLoading(false);
    }
  };

  const allEvidence = claims.reduce((acc, claim) => {
    return [...acc, ...(claim.evidence_details || [])];
  }, []);

  const hasClaims = claims.length > 0;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-slate-900">Verification Workspace</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Area */}
        <div className="space-y-4">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Enter AI-generated response or text to verify
            </label>
            <textarea
              className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              placeholder="Paste text here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              maxLength={5000}
            />
            <div className="flex justify-end mt-1">
              <span className={`text-xs ${text.length > 4500 ? 'text-red-500' : 'text-gray-400'}`}>
                {text.length} / 5000
              </span>
            </div>
            <button
              onClick={handleVerify}
              disabled={loading || !text.trim()}
              className={`mt-4 w-full py-3 px-6 rounded-lg font-semibold text-white transition ${
                loading || !text.trim() ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {loading ? 'Analyzing Claims...' : 'Verify Now'}
            </button>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 text-red-700">
              {error}
            </div>
          )}
        </div>

        {/* Results Area */}
        <div className="space-y-6">
          {/* Progress indicator while streaming */}
          {loading && totalClaims !== null && (
            <div className="bg-white p-4 rounded-xl shadow-md border border-gray-100">
              <div className="flex justify-between text-sm text-gray-600 mb-2">
                <span className="font-medium">Verifying claims...</span>
                <span>{claims.length} / {totalClaims}</span>
              </div>
              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-500 transition-all duration-500 rounded-full"
                  style={{ width: `${totalClaims > 0 ? (claims.length / totalClaims) * 100 : 0}%` }}
                />
              </div>
            </div>
          )}

          {loading && totalClaims === null && <Loader />}

          {hasClaims && (
            <>
              {isComplete && (
                <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                  <h2 className="text-xl font-bold mb-4">Verification Summary</h2>
                  {totalTimeMs && (
                    <div className="flex flex-wrap gap-4 mb-6">
                      <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 text-xs">
                        <span className="text-gray-500 font-medium uppercase">Total Time:</span>
                        <span className="ml-2 font-bold text-blue-600">{totalTimeMs}ms</span>
                      </div>
                      <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 text-xs">
                        <span className="text-gray-500 font-medium uppercase">Claims:</span>
                        <span className="ml-2 font-bold text-slate-700">{claims.length}</span>
                      </div>
                      {jobId && (
                        <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 text-xs">
                          <span className="text-gray-500 font-medium uppercase">Job ID:</span>
                          <span className="ml-2 font-bold text-slate-700">#{jobId}</span>
                        </div>
                      )}
                    </div>
                  )}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <ConfidenceMeter score={overallRisk} />
                    <div className="flex flex-col justify-center">
                      <div className="text-sm font-medium text-gray-500 uppercase">Analysis Results</div>
                      <div className="text-2xl font-bold text-slate-900">
                        {claims.length} Factual Claims
                      </div>
                      <p className="text-gray-500 text-sm mt-2">
                        {overallRisk < 0.3
                          ? 'The content appears to be highly reliable based on available evidence.'
                          : overallRisk < 0.7
                          ? 'Some claims may be inaccurate or lack sufficient evidence.'
                          : 'High probability of hallucinations detected in this response.'}
                      </p>
                    </div>
                  </div>
                  <DashboardChart claims={claims} />
                </div>
              )}

              {isComplete && <Heatmap text={text} claims={claims} />}

              <div className="space-y-4">
                <h2 className="text-xl font-bold">
                  Consensus Analysis ({claims.length}{pendingCount > 0 ? ` of ${totalClaims}` : ''})
                </h2>
                {claims.map((claim, index) => (
                  <ClaimCard key={index} data={claim} />
                ))}
                {pendingCount > 0 && (
                  <div className="p-4 rounded-xl border border-dashed border-blue-200 bg-blue-50 text-center text-sm text-blue-600 font-medium animate-pulse">
                    Analyzing {pendingCount} more claim{pendingCount > 1 ? 's' : ''}...
                  </div>
                )}
              </div>

              {isComplete && <EvidencePanel evidence={allEvidence} />}
            </>
          )}

          {!hasClaims && !loading && (
            <div className="bg-blue-50 border border-blue-100 p-8 rounded-xl text-center text-blue-800">
              <p className="text-lg font-medium">Ready for analysis</p>
              <p className="text-sm mt-2 opacity-75">Submit text on the left to start the verification process.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VerificationWorkspace;
