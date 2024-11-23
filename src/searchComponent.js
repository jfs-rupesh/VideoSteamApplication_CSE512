import React, { useState } from 'react';
import axios from 'axios';

const SearchComponent = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/api/search?query=${query}`);
            setResults(response.data.results);
        } catch (error) {
            console.error("Search error:", error);
        }
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Search videos"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button onClick={handleSearch}>Search</button>
            <ul>
                {results.map((result, index) => (
                    <li key={index}>
                        <a href={result.video_url} target="_blank" rel="noopener noreferrer">
                            {result.title}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchComponent;
