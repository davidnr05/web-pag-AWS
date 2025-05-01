import React, { useState } from 'react';
import CustomerSelect from './Components/CustomerSelect';
import StoreSelect from './Components/StoreSelect';
import MovieList from './Components/MovieList';
import './Styles/App.css';


function App() {
  const [selectedCustomer, setSelectedCustomer] = useState('');
  const [selectedStore, setSelectedStore] = useState('');

  const handleCustomerChange = (customerId) => {
    setSelectedCustomer(customerId);
    setSelectedStore('');
  };
  
  

  const handleStoreChange = (e) => {
    setSelectedStore(e.target.value);
  };

  const stores = [
    { store_id: 1 },
    { store_id: 2 }
  ];

  return (
    <div className="app-container">
      <h1>Alquiler de Películas</h1>
      <CustomerSelect onChange={handleCustomerChange} />
      {selectedCustomer && (
        <StoreSelect
          stores={stores}
          selectedStore={selectedStore}
          onChange={handleStoreChange}
        />
      )}
      {selectedCustomer && selectedStore && (
        <MovieList customerId={selectedCustomer} storeId={selectedStore} />
      )}
    </div>
  )};
  

export default App;
