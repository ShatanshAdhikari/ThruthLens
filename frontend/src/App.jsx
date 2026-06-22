import { useState } from 'react';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import VerificationWorkspace from './pages/VerificationWorkspace';
import Footer from './components/Footer';

function App() {
  const [currentPage, setCurrentPage] = useState('landing');

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar onNavigate={setCurrentPage} currentPage={currentPage} />
      
      <main className="flex-grow">
        {currentPage === 'landing' && (
          <LandingPage onStart={() => setCurrentPage('verify')} />
        )}
        
        {currentPage === 'verify' && (
          <VerificationWorkspace />
        )}
      </main>
      
      <Footer />
    </div>
  );
}

export default App;
