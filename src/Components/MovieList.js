import React, { useEffect, useState } from 'react';
import axios from 'axios';

const MovieList = ({ customerId, storeId }) => {
  const [movies, setMovies] = useState([]);
  const [rentedMovies, setRentedMovies] = useState([]);

  useEffect(() => {
    if (!storeId || !customerId) return;

    // Obtener películas disponibles
    axios.post('http://34.238.119.190:5000/available_movies', { store_id: storeId })
      .then(res => setMovies(res.data))
      .catch(err => console.error('Error fetching movies:', err));

    // Obtener películas rentadas por el cliente (sin devolver)
    axios.post('http://34.238.119.190:5000/rented_movies', {
      customer_id: customerId,
      store_id: storeId
    })
      .then(res => setRentedMovies(res.data))
      .catch(err => console.error('Error fetching rented movies:', err));
  }, [storeId, customerId]);

  const rentMovie = (filmId) => {
    axios.post('http://34.238.119.190:5000/rent', {
      film_id: filmId,
      customer_id: customerId
    })
      .then(res => {
        alert(res.data.message);
        window.location.reload(); // Actualiza la lista
      })
      .catch(err => {
        alert('Error al rentar: ' + err.response?.data?.error);
      });
  };

  const returnMovie = (filmId) => {
    axios.post('http://34.238.119.190:5000/return', {
      film_id: filmId,
      customer_id: customerId,
      store_id: storeId
    })
      .then(res => {
        alert(res.data.message);
        window.location.reload();
      })
      .catch(err => {
        alert('Error al devolver: ' + err.response?.data?.error);
      });
  };

  return (
    <div>
      <h2>Películas disponibles</h2>
      <ul>
        {movies.map(movie => (
          <li key={movie.film_id}>
            <strong>{movie.title}</strong>: {movie.description}
            {rentedMovies.some(r => r.film_id === movie.film_id) ? (
            <button className="return" onClick={() => returnMovie(movie.film_id)}>Devolver</button>
           ) : (
           <button className="rent" onClick={() => rentMovie(movie.film_id)}>Rentar</button>
          )}

          </li>
        ))}
      </ul>
    </div>
  );
};

export default MovieList;
