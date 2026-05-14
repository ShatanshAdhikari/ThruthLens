
const ClaimCard = ({ data }) => {
  const { claim, status, risk_score, evidence, source } = data;

  const getStatusColor = () => {
    switch (status) {
      case 'Supported': return 'bg-green-100 text-green-800 border-green-200';
      case 'Contradicted': return 'bg-red-100 text-red-800 border-red-200';
      case 'Insufficient Evidence': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className={`p-5 rounded-xl border-l-4 shadow-sm ${getStatusColor()} bg-white transition-all hover:shadow-md`}>
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-lg text-slate-800">{claim}</h3>
        <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${getStatusColor()}`}>
          {status}
        </span>
      </div>
      
      {evidence && (
        <div className="mt-4 bg-gray-50 p-3 rounded-lg border border-gray-200">
          <div className="text-xs font-bold text-gray-500 uppercase mb-1">Evidence Source: {source}</div>
          <p className="text-sm text-gray-700 italic">"{evidence}"</p>
        </div>
      )}
      
      <div className="mt-4 flex items-center space-x-2">
        <div className="text-xs font-bold text-gray-500 uppercase">Risk Score:</div>
        <div className="w-full bg-gray-200 rounded-full h-2 flex-grow max-w-[100px]">
          <div 
            className={`h-2 rounded-full ${risk_score > 0.7 ? 'bg-red-500' : risk_score > 0.3 ? 'bg-yellow-500' : 'bg-green-500'}`}
            style={{ width: `${risk_score * 100}%` }}
          ></div>
        </div>
        <div className="text-xs font-semibold">{(risk_score * 100).toFixed(0)}%</div>
      </div>
    </div>
  );
};

export default ClaimCard;
