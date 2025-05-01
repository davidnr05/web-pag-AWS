import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CustomerSelect = ({ onChange }) => {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    axios.get("http://34.238.119.190:5000/customers")
      .then(res => {
        console.log("Clientes recibidos:", res.data);
        setCustomers(res.data);
      })
      .catch(err => console.error("Error al obtener clientes:", err));
  }, []);
  

  return (
    <div>
      <h2>Seleccionar Cliente</h2>
      <select onChange={e => onChange(e.target.value)}>
        <option value="">-- Selecciona un cliente --</option>
        {customers.map(c => (
          <option key={c.customer_id} value={c.customer_id}>
            {c.first_name} {c.last_name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default CustomerSelect;
