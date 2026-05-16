
import heroImage from '../assets/hero.png';

const HeroSection = ({ onStart }) => {
  return (
    <div className="relative overflow-hidden bg-white pt-16 pb-32">
      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-12 lg:gap-8">
          <div className="sm:text-center md:mx-auto md:max-w-2xl lg:col-span-6 lg:text-left">
            <h1>
              <span className="block text-base font-semibold text-blue-600 sm:text-lg lg:text-base xl:text-lg">
                Introducing TruthLens
              </span>
              <span className="mt-1 block text-4xl font-bold tracking-tight sm:text-5xl xl:text-6xl">
                <span className="block text-slate-900">Verify AI Claims</span>
                <span className="block text-blue-600">Eliminate Hallucinations</span>
              </span>
            </h1>
            <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-xl lg:text-lg xl:text-xl">
              TruthLens is an intelligent verification layer for LLMs. We extract factual claims, 
              retrieve supporting evidence, and perform semantic verification to ensure your 
              AI outputs are accurate and trustworthy.
            </p>
            <div className="mt-8 sm:mx-auto sm:max-w-lg sm:text-center lg:mx-0 lg:text-left">
              <button
                onClick={onStart}
                className="inline-flex items-center rounded-md border border-transparent bg-blue-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Launch Workspace
              </button>
              <a
                href="#how-it-works"
                className="ml-4 inline-flex items-center rounded-md border border-gray-300 bg-white px-6 py-3 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                View Documentation
              </a>
            </div>
          </div>
          <div className="relative mt-12 sm:mx-auto sm:max-w-2xl lg:col-span-6 lg:mx-0 lg:mt-0 lg:flex lg:items-center">
            <div className="relative mx-auto w-full rounded-2xl shadow-2xl lg:max-w-xl overflow-hidden group">
              <div className="relative block w-full aspect-video bg-slate-900 focus:outline-none">
                <img
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                  src="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80"
                  alt="Distorted AI Data Visual"
                />
                <div className="absolute inset-0 bg-gradient-to-tr from-blue-600/20 to-transparent pointer-events-none"></div>
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="h-32 w-32 rounded-full bg-blue-500/10 animate-ping"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
