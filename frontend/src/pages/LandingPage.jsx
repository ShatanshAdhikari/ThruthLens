import HeroSection from '../components/HeroSection';

const LandingPage = ({ onStart }) => {
  return (
    <div className="bg-white">
      <HeroSection onStart={onStart} />

      {/* Features Section */}
      <div id="features" className="py-24 sm:py-32 bg-slate-50">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-blue-600 uppercase tracking-widest">Core Features</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Everything you need to trust AI output
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
              <div className="flex flex-col bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
                <dt className="flex items-center gap-x-3 text-lg font-bold leading-7 text-slate-900">
                  <svg className="h-6 w-6 flex-none text-blue-600" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                  </svg>
                  Claim Extraction
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">Atomic factual claims are automatically identified and separated from conversational filler using advanced NLP parsing.</p>
                </dd>
              </div>
              <div className="flex flex-col bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
                <dt className="flex items-center gap-x-3 text-lg font-bold leading-7 text-slate-900">
                  <svg className="h-6 w-6 flex-none text-blue-600" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9s2.015-9 4.5-9m0 0a9.015 9.015 0 010 18z" />
                  </svg>
                  Semantic Search
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">Claims are verified against high-quality evidence retrieved from trusted knowledge bases and verified corpora.</p>
                </dd>
              </div>
              <div className="flex flex-col bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
                <dt className="flex items-center gap-x-3 text-lg font-bold leading-7 text-slate-900">
                  <svg className="h-6 w-6 flex-none text-blue-600" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Risk Scoring
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">Advanced NLI models estimate the probability of hallucination with clear, explainable labels and confidence scores.</p>
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>

      {/* How it Works Section */}
      <div id="how-it-works" className="py-24 bg-white overflow-hidden">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center mb-16">
            <h2 className="text-base font-semibold leading-7 text-blue-600 uppercase tracking-widest">How It Works</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              The CAR Verification Pipeline
            </p>
            <p className="mt-4 text-gray-500">
              Every submission passes through four rigorous stages to produce a transparent, auditable verdict.
            </p>
          </div>
          <div className="relative">
            {/* Connector line */}
            <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-100 hidden lg:block" aria-hidden="true" />
            <div className="space-y-12 lg:space-y-0 lg:grid lg:grid-cols-2 lg:gap-x-16 lg:gap-y-12">
              {[
                {
                  step: '01',
                  title: 'Deep Claim Deconstruction',
                  description: 'An LLM (Llama3) breaks the input into atomic factual statements, resolving pronouns and maintaining context so every claim is self-contained and verifiable.',
                  icon: (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                    </svg>
                  ),
                },
                {
                  step: '02',
                  title: 'Multi-Perspective Search',
                  description: 'Three targeted queries per claim harvest evidence from Tavily, Google Fact Check, and DuckDuckGo — supporting, contradicting, and contextual angles simultaneously.',
                  icon: (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  ),
                },
                {
                  step: '03',
                  title: 'Consensus-Audit-Reasoning Engine',
                  description: 'A DeBERTa NLI cross-encoder individually scores each source. A Judge Agent LLM then weighs source authority, resolves contradictions, and delivers a final verdict with full reasoning.',
                  icon: (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  ),
                },
                {
                  step: '04',
                  title: 'Relational Audit Trail',
                  description: 'Every claim, source URL, individual NLI verdict, and the Judge\'s reasoning chain are persisted to a database, giving you a complete, reproducible record of every verification.',
                  icon: (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                    </svg>
                  ),
                },
              ].map((item) => (
                <div key={item.step} className="relative flex gap-6 bg-white p-8 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex-shrink-0 w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center text-white">
                    {item.icon}
                  </div>
                  <div>
                    <div className="text-xs font-black text-blue-400 uppercase tracking-widest mb-1">Step {item.step}</div>
                    <h3 className="text-lg font-bold text-slate-900 mb-2">{item.title}</h3>
                    <p className="text-gray-500 text-sm leading-relaxed">{item.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Knowledge Base Section - Target for "Resources" */}
      <div id="resources" className="py-24 bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-base font-semibold leading-7 text-blue-400 uppercase tracking-widest">Global Evidence Base</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Verified Knowledge Sources
            </p>
            <p className="mt-4 text-slate-400 max-w-2xl mx-auto">
              TruthLens cross-references every AI claim against a multi-modal knowledge graph built from the world's most trusted data repositories.
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 hover:border-blue-500 transition-colors">
              <div className="text-blue-400 font-bold mb-2">Encyclopedic</div>
              <div className="text-xl font-bold">Wikipedia</div>
              <div className="text-xs text-slate-500 mt-2">6M+ Verified Articles</div>
            </div>
            <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 hover:border-blue-500 transition-colors">
              <div className="text-blue-400 font-bold mb-2">Scientific</div>
              <div className="text-xl font-bold">ArXiv.org</div>
              <div className="text-xs text-slate-500 mt-2">2M+ Research Papers</div>
            </div>
            <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 hover:border-blue-500 transition-colors">
              <div className="text-blue-400 font-bold mb-2">Medical</div>
              <div className="text-xl font-bold">PubMed</div>
              <div className="text-xs text-slate-500 mt-2">35M+ Citations</div>
            </div>
            <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 hover:border-blue-500 transition-colors">
              <div className="text-blue-400 font-bold mb-2">Web Archive</div>
              <div className="text-xl font-bold">Common Crawl</div>
              <div className="text-xs text-slate-500 mt-2">Petabytes of Web Data</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
