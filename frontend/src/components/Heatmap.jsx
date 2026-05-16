
const Heatmap = ({ text, claims }) => {
  if (!text || !claims) return null;

  // Sort claims by start position
  const sortedClaims = [...claims].sort((a, b) => a.start - b.start);

  const renderHighlightedText = () => {
    const elements = [];
    let lastIndex = 0;

    sortedClaims.forEach((claim, index) => {
      // Add text before the claim
      if (claim.start > lastIndex) {
        elements.push(
          <span key={`text-${lastIndex}`}>
            {text.substring(lastIndex, claim.start)}
          </span>
        );
      }

      // Determine color based on risk score
      const getColorClass = (score) => {
        if (score > 0.7) return 'bg-red-200 text-red-900 border-b-2 border-red-500';
        if (score > 0.3) return 'bg-yellow-200 text-yellow-900 border-b-2 border-yellow-500';
        return 'bg-green-200 text-green-900 border-b-2 border-green-500';
      };

      // Add the highlighted claim
      elements.push(
        <mark
          key={`claim-${index}`}
          className={`px-1 rounded-sm cursor-help transition-all hover:brightness-95 ${getColorClass(claim.risk_score)}`}
          title={`${claim.status} (Risk: ${(claim.risk_score * 100).toFixed(0)}%)`}
        >
          {text.substring(claim.start, claim.end)}
        </mark>
      );

      lastIndex = claim.end;
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
