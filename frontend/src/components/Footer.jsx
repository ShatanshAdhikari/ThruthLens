
const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 py-12 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">TL</div>
            <span className="text-xl font-bold text-slate-900 tracking-tight">TruthLens</span>
          </div>
          <p className="mt-8 md:mt-0 text-base text-gray-400">
            &copy; 2026 TruthLens AI. All rights reserved. Built for AI Reliability.
          </p>
          <div className="mt-8 md:mt-0 flex space-x-6">
            <a href="#" className="text-gray-400 hover:text-gray-500">Privacy</a>
            <a href="#" className="text-gray-400 hover:text-gray-500">Terms</a>
            <a href="#" className="text-gray-400 hover:text-gray-500">GitHub</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
