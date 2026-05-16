
const ConfidenceMeter = ({ score }) => {
  // score is 0 to 1
  const percentage = (score * 100).toFixed(0);
  
  const getStatus = () => {
    if (score > 0.7) return 'High Risk';
    if (score > 0.3) return 'Moderate Risk';
    return 'Low Risk';
  };

  return (
    <div className="flex flex-col items-center justify-center p-4 bg-slate-50 rounded-xl border border-slate-200">
      <div className="relative w-32 h-32">
        <svg className="w-full h-full" viewBox="0 0 36 36">
          <path
            className="text-gray-200"
            strokeDasharray="100, 100"
            strokeWidth="3"
            stroke="currentColor"
            fill="none"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <path
            className={`transition-all duration-1000 ease-out text-blue-600`}
            strokeDasharray={`${percentage}, 100`}
            strokeWidth="3"
            strokeLinecap="round"
            stroke="currentColor"
            fill="none"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <text x="18" y="20.35" className="text-xs font-bold" textAnchor="middle" fill="#334155">{percentage}%</text>
        </svg>
      </div>
      <div className={`mt-2 text-sm font-bold uppercase tracking-widest ${score > 0.7 ? 'text-red-600' : score > 0.3 ? 'text-yellow-600' : 'text-green-600'}`}>
        {getStatus()}
      </div>
    </div>
  );
};

export default ConfidenceMeter;
