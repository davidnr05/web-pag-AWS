import React from 'react';

const StoreSelect = ({ stores, selectedStore, onChange }) => {
  return (
    <div>
      <h2>Seleccionar Tienda</h2>
      <select value={selectedStore} onChange={onChange}>
        <option value="">-- Selecciona una tienda --</option>
        {stores.map(store => (
          <option key={store.store_id} value={store.store_id}>
            {store.store_id === 1 ? 'Tienda A' : 'Tienda B'} (ID: {store.store_id})
          </option>
        ))}
      </select>
    </div>
  );
};

export default StoreSelect;
