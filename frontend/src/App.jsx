import { useState } from 'react';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import VerificationWorkspace from './pages/VerificationWorkspace';

function App() {
  const [currentPage, setCurrentPage] = useState('landing');

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar onNavigate={setCurrentPage} />
      
      {currentPage === 'landing' && (
        <LandingPage onStart={() => setCurrentPage('verify')} />
      )}
      
      {currentPage === 'verify' && (
        <VerificationWorkspace />
      )}
      
      {/* Footer can be added here */}
    </div>
  );
}

export default App;
