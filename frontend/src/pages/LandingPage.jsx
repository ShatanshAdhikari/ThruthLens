
const LandingPage = ({ onStart }) => {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative isolate overflow-hidden bg-gradient-to-b from-blue-100/20 pt-14">
        <div className="mx-auto max-w-7xl px-6 py-32 sm:py-40 lg:px-8">
          <div className="mx-auto max-w-2xl lg:mx-0 lg:grid lg:max-w-none lg:grid-cols-2 lg:gap-x-16 lg:gap-y-6 xl:grid-cols-1 xl:grid-rows-1 xl:gap-x-8">
            <h1 className="max-w-2xl text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl lg:col-span-2 xl:col-auto">
              Verify AI Responses with Confidence.
            </h1>
            <div className="mt-6 max-w-xl lg:mt-0 xl:col-end-1 xl:row-start-1">
              <p className="text-lg leading-8 text-gray-600">
                TruthLens detects hallucinations and factual inaccuracies in AI-generated content. 
                Our platform extracts claims, retrieves supporting evidence, and provides an explainable risk score.
              </p>
              <div className="mt-10 flex items-center gap-x-6">
                <button
                  onClick={onStart}
                  className="rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
                >
                  Get started
                </button>
                <a href="#features" className="text-sm font-semibold leading-6 text-slate-900">
                  Live demo <span aria-hidden="true">→</span>
                </a>
              </div>
            </div>
            <div className="mt-14 flex justify-end gap-8 sm:-mt-44 sm:justify-start sm:pl-20 lg:mt-0 lg:pl-0">
               {/* Visual placeholder */}
               <div className="w-full max-w-md bg-blue-600 h-64 rounded-2xl shadow-2xl flex items-center justify-center text-white text-6xl font-black">
                 TL
               </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-blue-600">Faster Verification</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Everything you need to trust AI output
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-slate-900">
                  <div className="h-5 w-5 flex-none text-blue-600" />
                  Claim Extraction
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">Atomic factual claims are automatically identified and separated from conversational filler.</p>
                </dd>
              </div>
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-slate-900">
                   <div className="h-5 w-5 flex-none text-blue-600" />
                  Semantic Search
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">Claims are verified against high-quality evidence retrieved from trusted knowledge bases.</p>
                </dd>
              </div>
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-slate-900">
                   <div className="h-5 w-5 flex-none text-blue-600" />
                  Risk Scoring
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">Advanced NLI models estimate the probability of hallucination with clear, explainable labels.</p>
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
