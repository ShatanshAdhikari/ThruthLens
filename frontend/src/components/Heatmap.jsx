
const Heatmap = ({ text, claims }) => {
  if (!text || !claims) return null;

  // 1. Group claims by their text range (start/end)
  const rangeMap = {};
  claims.forEach(c => {
    const key = `${c.start}-${c.end}`;
    if (!rangeMap[key]) {
      rangeMap[key] = { ...c, count: 1 };
    } else {
      // Keep the most severe risk/status
      if (c.risk_score > rangeMap[key].risk_score) {
        rangeMap[key].risk_score = c.risk_score;
        rangeMap[key].status = c.status;
      }
      rangeMap[key].count += 1;
    }
  });

  // 2. Convert back to array and sort
  const uniqueRanges = Object.values(rangeMap).sort((a, b) => a.start - b.start);

  const renderHighlightedText = () => {
    const elements = [];
    let lastIndex = 0;

    uniqueRanges.forEach((range, index) => {
      // Add text before the range
      if (range.start > lastIndex) {
        elements.push(
          <span key={`text-${lastIndex}`}>
            {text.substring(lastIndex, range.start)}
          </span>
        );
      }

      // Determine color based on risk score
      const getColorClass = (score) => {
        if (score > 0.7) return 'bg-red-200 text-red-900 border-b-2 border-red-400';
        if (score > 0.3) return 'bg-yellow-200 text-yellow-900 border-b-2 border-yellow-400';
        return 'bg-green-200 text-green-900 border-b-2 border-green-400';
      };

      // Add the highlighted range
      elements.push(
        <mark
          key={`range-${index}`}
          className={`px-1 rounded-sm cursor-help transition-all hover:brightness-95 relative group ${getColorClass(range.risk_score)}`}
        >
          {text.substring(range.start, range.end)}
          
          {/* Custom Tooltip */}
          <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block z-50 w-48 bg-slate-800 text-white text-[10px] p-2 rounded shadow-xl pointer-events-none">
            <div className="font-bold border-b border-slate-600 pb-1 mb-1 uppercase tracking-tighter">
              {range.count > 1 ? `${range.count} Claims Found` : 'Clinical Status'}
            </div>
            <div className="flex justify-between items-center">
              <span>{range.status}</span>
              <span className="font-mono">{(range.risk_score * 100).toFixed(0)}% Risk</span>
            </div>
          </span>
        </mark>
      );

      lastIndex = range.end;
    });

    // Add remaining text
    if (lastIndex < text.length) {
      elements.push(
        <span key={`text-${lastIndex}`}>
          {text.substring(lastIndex)}
        </span>
      );
    }

    return elements;
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
      <h2 className="text-xl font-bold mb-4">Risk Heatmap</h2>
      <div className="prose prose-slate max-w-none leading-relaxed text-lg p-4 bg-slate-50 rounded-lg border border-slate-100">
        {renderHighlightedText()}
      </div>
      <div className="mt-4 flex space-x-4 text-xs font-semibold uppercase tracking-wider">
        <div className="flex items-center">
          <span className="w-3 h-3 bg-green-200 border-b-2 border-green-500 mr-2"></span>
          <span>Supported</span>
        </div>
        <div className="flex items-center">
          <span className="w-3 h-3 bg-yellow-200 border-b-2 border-yellow-500 mr-2"></span>
          <span>Uncertain</span>
        </div>
        <div className="flex items-center">
          <span className="w-3 h-3 bg-red-200 border-b-2 border-red-500 mr-2"></span>
          <span>Contradicted</span>
        </div>
      </div>
    </div>
  );
};

export default Heatmap;
