import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import CaseRegistration from './components/CaseRegistration';
import MatchResults from './components/MatchResults';
import './App.css';

function App() {
    const [currentView, setCurrentView] = useState('upload');
    const [matchResults, setMatchResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleUploadSuccess = (data) => {
        setLoading(false);
        if (data.success) {
            setMatchResults(data.matches);
        }
    };

    const handleUploadStart = () => {
        setLoading(true);
        setMatchResults(null);
    };

    return (
        <div className="App">
            <header className="app-header">
                <h1>Missing Person Finder</h1>
                <nav>
                    <button 
                        onClick={() => setCurrentView('upload')}
                        className={currentView === 'upload' ? 'active' : ''}
                    >
                        Find Match
                    </button>
                    <button 
                        onClick={() => setCurrentView('register')}
                        className={currentView === 'register' ? 'active' : ''}
                    >
                        Register Case
                    </button>
                </nav>
            </header>

            <main className="app-main">
                {currentView === 'upload' && (
                    <div className="upload-section">
                        <ImageUpload 
                            onUploadSuccess={handleUploadSuccess}
                            onUploadStart={handleUploadStart}
                        />
                        <MatchResults matches={matchResults} loading={loading} />
                    </div>
                )}

                {currentView === 'register' && (
                    <CaseRegistration 
                        onRegistrationSuccess={(data) => {
                            alert('Case registered successfully!');
                        }}
                    />
                )}
            </main>
        </div>
    );
}

export default App;
