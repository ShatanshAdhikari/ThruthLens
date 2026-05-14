import { useState } from 'react';
import axios from 'axios';
import ClaimCard from '../components/ClaimCard';
import Loader from '../components/Loader';
import DashboardChart from '../components/DashboardChart';

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
      const response = await axios.post('http://localhost:8000/api/verify', { text });
      setResults(response.data);
    } catch (err) {
      setError('Failed to verify text. Please ensure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

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
            />
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
                <div className="flex items-center space-x-6 mb-6">
                  <div className="text-4xl font-bold text-blue-600">
                    {(results.overall_risk * 100).toFixed(0)}%
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-500 uppercase">Overall Risk Score</div>
                    <div className="text-lg font-semibold">
                      {results.overall_risk > 0.7 ? 'High Risk' : results.overall_risk > 0.3 ? 'Moderate Risk' : 'Low Risk'}
                    </div>
                  </div>
                </div>
                <DashboardChart claims={results.claims} />
              </div>

              <div className="space-y-4">
                <h2 className="text-xl font-bold">Extracted Claims ({results.claims.length})</h2>
                {results.claims.map((claim, index) => (
                  <ClaimCard key={index} data={claim} />
                ))}
              </div>
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
