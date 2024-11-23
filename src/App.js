import React, { useState } from 'react';
import VideoPlayer from './videoPlayer';
import SearchComponent from './searchComponent';
import './App.css'; // Importing the CSS file for styling
import logo from './logo.png'; // Import your logo image

function App() {
    const [videoUrl, setVideoUrl] = useState("");

    return (
        <div className="App">
            {/* Header Section */}
            <header className="App-header">
                <img src={logo} alt="App Logo" className="App-logo" />
                <h1>Video Streaming App</h1>
            </header>

            {/* Search Section */}
            <section className="Search-section">
                <SearchComponent setVideoUrl={setVideoUrl} />
            </section>

            {/* Manual URL Input Section */}
            <section className="URL-section">
                <h2>Play Video by URL</h2>
                <input
                    className="URL-input"
                    type="text"
                    placeholder="Enter video URL (.m3u8)"
                    value={videoUrl}
                    onChange={(e) => setVideoUrl(e.target.value)}
                />
            </section>

            {/* Video Player Section */}
            <section className="Video-section">
                <VideoPlayer videoUrl={videoUrl} />
            </section>

            {/* Footer */}
            <footer className="App-footer">
                <p>&copy; 2024 Video Streaming App. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default App;
