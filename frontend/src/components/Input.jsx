import React from 'react'
import { useState, useRef, useEffect } from 'react';

const Input = ({onSearch, data}) => {

    const [movie, setMovie] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const containerRef = useRef(null);

    const handleInputChange = (e) => {
        const value = e.target.value;
        setMovie(value);
        //console.log(data)
        // Update suggestions based on user input
        if (value) {
            const filteredMovies = data.filter(m => 
                m.title.toLowerCase().includes(value.toLowerCase())
            );
            setSuggestions(filteredMovies); // Show top 5 matches
        } else {
            setSuggestions([]);
        }
    };

    const handleSearch = () => {
        onSearch(movie);
    }

    const handleSuggestionClick = (suggestedMovie) => {
        setMovie(suggestedMovie.title); // Set the input to the clicked suggestion
        setSuggestions([]); // Clear the suggestions
    };

    useEffect(() => {
        function handleClickOutside(event) {
            if (containerRef.current && !containerRef.current.contains(event.target)) {
                setSuggestions([]);  // hide suggestions if click was outside
            }
        }

        // Attach the listeners on component mount
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            // Detach the listener on component unmount
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [containerRef]);

    return (
        <div className='container' ref={containerRef}> 
            <input 
                type="text"
                placeholder="Enter movie name..."
                value={movie}
                onChange={handleInputChange}
                className='bar'
            />
            {suggestions.length > 0 && (
                <ul className='suggestions-list'>
                    {suggestions.map((suggestedMovie,index) => (
                        <li
                          key = {index}
                          onClick={()=> handleSuggestionClick(suggestedMovie)}
                          className='suggestion-item'
                        >
                            {suggestedMovie.title}
                        </li>
                    ))}
                </ul>
            )}
            <button onClick={handleSearch} className='button'>Recommend</button>
        </div>
    );
}

export default Input