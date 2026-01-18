import React, { useState, useEffect, useRef } from 'react';
import { searchLocation } from '../../services/api';

const SearchBox = ({ onLocationSelect }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const searchContainerRef = useRef(null);

  useEffect(() => {
    if (!searchQuery) {
      setSuggestions([]);
      return;
    }

    const handler = setTimeout(async () => {
      const results = await searchLocation(searchQuery);
      setSuggestions(results);
    }, 500);

    return () => {
      clearTimeout(handler);
    };
  }, [searchQuery]);

  useEffect(() => {
    function handleClickOutside(event) {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target)) {
        setSuggestions([]);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [searchContainerRef]);

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  const handleSearch = async () => {
    if (!searchQuery) {
      alert('Please enter an address to search.');
      return;
    }
    setSuggestions([]);

    const results = await searchLocation(searchQuery);
    
    if (results.length === 0) {
      alert('Could not find the location you entered. Please try again.');
      return;
    }

    const searchCoords = results[0].center;
    onLocationSelect(searchCoords);
  };

  return (
    <div className="search-container" ref={searchContainerRef}>
      <input 
        type="text" 
        className="parking-query" 
        placeholder="Search for parking..." 
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onKeyPress={handleKeyPress}
      />
      {suggestions.length > 0 && (
        <div className="suggestions-container">
          {suggestions.map((suggestion, index) => (
            <div 
              key={index} 
              className="suggestion-item"
              onClick={() => {
                setSearchQuery(suggestion.place_name);
                setSuggestions([]);
              }}
            >
              {suggestion.place_name}
            </div>
          ))}
        </div>
      )}
      <button id="find-nearest-btn" onClick={handleSearch}>
        GO
        <span className="arrow-icon"></span>
      </button>
    </div>
  );
};

export default SearchBox;
