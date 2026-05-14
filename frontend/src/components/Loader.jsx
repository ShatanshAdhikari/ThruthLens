
const Loader = () => {
  return (
    <div className="flex flex-col items-center justify-center p-12 bg-white rounded-xl shadow-md border border-gray-100">
      <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600 mb-4"></div>
      <p className="text-gray-600 font-medium animate-pulse">Analyzing factual consistency...</p>
      <p className="text-sm text-gray-400 mt-2">Connecting to TruthLens AI Pipeline</p>
    </div>
  );
};

export default Loader;
