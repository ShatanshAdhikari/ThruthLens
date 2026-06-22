import { useState } from 'react';
import axios from 'axios';
import ClaimCard from '../components/ClaimCard';
import Loader from '../components/Loader';
import DashboardChart from '../components/DashboardChart';
import Heatmap from '../components/Heatmap';
import ConfidenceMeter from '../components/ConfidenceMeter';
import EvidencePanel from '../components/EvidencePanel';

const VerificationWorkspace = () => {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleVerify = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('/api/verify', { text });
      setResults(response.data);
    } catch (err) {
      setError('Failed to verify text. Please ensure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Helper to collect all evidence from all claims
  const allEvidence = (results?.claims || []).reduce((acc, claim) => {
    return [...acc, ...(claim.evidence_details || [])];
  }, []);

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
          {loading && <Loader />}
          
          {results && (
            <>
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <h2 className="text-xl font-bold mb-4">Verification Summary</h2>
                {results.metadata && (
                  <div className="flex flex-wrap gap-4 mb-6">
                    <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 text-xs">
                      <span className="text-gray-500 font-medium uppercase">Total Time:</span>
                      <span className="ml-2 font-bold text-blue-600">{results.metadata.total_time_ms}ms</span>
                    </div>
                    <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 text-xs">
                      <span className="text-gray-500 font-medium uppercase">Extraction:</span>
                      <span className="ml-2 font-bold text-slate-700">{results.metadata.extraction_time_ms}ms</span>
                    </div>
                    <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 text-xs">
                      <span className="text-gray-500 font-medium uppercase">Retrieval:</span>
                      <span className="ml-2 font-bold text-slate-700">{results.metadata.retrieval_time_ms}ms</span>
                    </div>
                    <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 text-xs">
                      <span className="text-gray-500 font-medium uppercase">Verification:</span>
                      <span className="ml-2 font-bold text-slate-700">{results.metadata.verification_time_ms}ms</span>
                    </div>
                    <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 text-xs">
                      <span className="text-gray-500 font-medium uppercase">Explainability:</span>
                      <span className="ml-2 font-bold text-slate-700">{results.metadata.explanation_time_ms}ms</span>
                    </div>
                  </div>
                )}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <ConfidenceMeter score={results.overall_risk} />
                  <div className="flex flex-col justify-center">
                    <div className="text-sm font-medium text-gray-500 uppercase">Analysis Results</div>
                    <div className="text-2xl font-bold text-slate-900">
                      {results.claims.length} Factual Claims
                    </div>
                    <p className="text-gray-500 text-sm mt-2">
                      {results.overall_risk < 0.3 
                        ? 'The content appears to be highly reliable based on available evidence.' 
                        : results.overall_risk < 0.7 
                        ? 'Some claims may be inaccurate or lack sufficient evidence.' 
                        : 'High probability of hallucinations detected in this response.'}
                    </p>
                  </div>
                </div>
                <DashboardChart claims={results.claims} />
              </div>

              <Heatmap text={results.text} claims={results.claims} />

              <div className="space-y-4">
                <h2 className="text-xl font-bold">Consensus Analysis ({results.claims.length})</h2>
                {results.claims.map((claim, index) => (
                  <ClaimCard key={index} data={claim} />
                ))}
              </div>

              <EvidencePanel evidence={allEvidence} />
            </>
          )}

          {!results && !loading && (
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
