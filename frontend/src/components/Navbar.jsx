
const Navbar = ({ onNavigate }) => {
  return (
    <nav className="bg-slate-900 text-white p-4 sticky top-0 z-50 shadow-lg">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-4">
        <div 
          className="text-2xl font-bold cursor-pointer flex items-center space-x-2"
          onClick={() => onNavigate('landing')}
        >
          <span className="bg-blue-600 px-2 py-1 rounded text-white mr-2">TL</span>
          <span>TruthLens</span>
        </div>
        <div className="hidden md:flex space-x-8">
          <button 
            onClick={() => onNavigate('landing')} 
            className="text-sm font-medium hover:text-blue-400 transition"
          >
            Product
          </button>
          <button 
            onClick={() => onNavigate('verify')} 
            className="text-sm font-medium hover:text-blue-400 transition"
          >
            Verify
          </button>
          <button 
            className="text-sm font-medium hover:text-blue-400 transition"
          >
            Resources
          </button>
        </div>
        <div>
          <button 
            onClick={() => onNavigate('verify')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-bold transition"
          >
            Try for Free
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
