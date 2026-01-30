import React, { useEffect, useState } from 'react';
import api from '../api/client';
import { toast } from 'react-toastify';

const InventoryList = () => {
    const [items, setItems] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [newItem, setNewItem] = useState({ name: '', sku: '', quantity: 0, description: '' });

    const fetchItems = async () => {
        try {
            const response = await api.get('/inventory');
            setItems(response.data);
        } catch (error) {
            toast.error('Failed to fetch inventory');
        }
    };

    useEffect(() => {
        fetchItems();
    }, []);

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await api.post('/inventory', newItem);
            toast.success('Item created');
            setShowModal(false);
            setNewItem({ name: '', sku: '', quantity: 0, description: '' });
            fetchItems();
        } catch (error) {
            toast.error('Failed to create item');
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', marginTop: '2rem' }}>
                <h1>Inventory</h1>
                <button className="btn btn-primary" onClick={() => setShowModal(!showModal)}>
                    {showModal ? 'Cancel' : 'Add Item'}
                </button>
            </div>

            {showModal && (
                <div className="card" style={{ marginBottom: '2rem' }}>
                    <h3>Add New Item</h3>
                    <form onSubmit={handleCreate}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div>
                                <label>Name</label>
                                <input value={newItem.name} onChange={(e) => setNewItem({ ...newItem, name: e.target.value })} required />
                            </div>
                            <div>
                                <label>SKU</label>
                                <input value={newItem.sku} onChange={(e) => setNewItem({ ...newItem, sku: e.target.value })} required />
                            </div>
                            <div>
                                <label>Quantity</label>
                                <input type="number" value={newItem.quantity} onChange={(e) => setNewItem({ ...newItem, quantity: parseInt(e.target.value) })} required />
                            </div>
                            <div>
                                <label>Description</label>
                                <input value={newItem.description} onChange={(e) => setNewItem({ ...newItem, description: e.target.value })} />
                            </div>
                        </div>
                        <button type="submit" className="btn btn-primary">Save Item</button>
                    </form>
                </div>
            )}

            <div className="card table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>SKU</th>
                            <th>Quantity</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items.map((item) => (
                            <tr key={item.id}>
                                <td style={{ fontWeight: '500' }}>{item.name}</td>
                                <td style={{ fontFamily: 'monospace' }}>{item.sku}</td>
                                <td>{item.quantity}</td>
                                <td>
                                    {item.quantity > 10 ? (
                                        <span className="badge badge-confirmed">In Stock</span>
                                    ) : item.quantity > 0 ? (
                                        <span className="badge badge-pending">Low Stock</span>
                                    ) : (
                                        <span className="badge badge-cancelled">Out of Stock</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default InventoryList;
