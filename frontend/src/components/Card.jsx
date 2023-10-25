import React from 'react'

const Card = ({movie,poster}) => {
  return (
    <div className="movie-card">
        <img src={poster} alt={`${movie} poster`} className="movie-poster" />
        <h2>{movie}</h2>
    </div>
  )
}

export default Card