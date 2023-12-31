import React, { useEffect } from 'react'
import { useState } from 'react'
import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import Input from './components/Input.jsx'
import Card from './components/Card.jsx'
import axios from 'axios'
import './App.css'


const App = () => {
  const [movies, setMovies] = useState([]);
  const [data,setData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(()=>{
    const fetchMovies = async ()=>{
      try {
        const res = await axios.get('http://localhost:5000/movies');
        setData(res.data.map(title => ({title})));
      } catch (error) {
        console.log(error);
      }
    }
    fetchMovies();
  },[])

  //console.log(data)
  const handleSearch = async (movie) => {
      setLoading(true);
      try {
        const response = await axios.post('http://localhost:5000/recommend', {
          movie_name: movie
        });
      setMovies(response.data);
      //console.log(movies)
      setError(null); // Clear any previous error
      setLoading(false);
  } catch (err) {
      console.error("There was an error fetching the recommendations:", err);
      setError("Failed to fetch movie recommendations. Please try again later.");
      setMovies([]); // Clear previous movies if any
  }
  }
  return (
    <div className="App">
        <Header />
        <Input onSearch={handleSearch} data = {data}/>
        <div className="movies-container">
            {loading ? <p>Loading recommendations...</p> :
            movies.recommendations && movies.recommendations.map((movie, index) => (
                <Card key={index} movie={movie} poster={movies.posters[index]}/>
            ))}
        </div>
        <Footer />
    </div>
  )
}

export default App
