import React from 'react';

const MatchResults = ({ matches, loading }) => {
    if (loading) {
        return <div className="loading">Searching for matches...</div>;
    }

    if (!matches || matches.length === 0) {
        return <div className="no-matches">No matches found.</div>;
    }

    return (
        <div className="match-results">
            <h3>Potential Matches Found</h3>
            <div className="matches-container">
                {matches.map((match, index) => (
                    <div key={index} className="match-card">
                        <div className="match-info">
                            <h4>{match.name}</h4>
                            <p><strong>Age:</strong> {match.age}</p>
                            <p><strong>Location:</strong> {match.location}</p>
                            <p><strong>Similarity:</strong> {(match.similarity_score * 100).toFixed(2)}%</p>
                        </div>
                        <div className="match-score">
                            <div 
                                className="score-bar"
                                style={{
                                    width: `${match.similarity_score * 100}%`,
                                    backgroundColor: match.similarity_score > 0.8 ? '#4CAF50' : 
                                                   match.similarity_score > 0.6 ? '#FF9800' : '#F44336'
                                }}
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MatchResults;
