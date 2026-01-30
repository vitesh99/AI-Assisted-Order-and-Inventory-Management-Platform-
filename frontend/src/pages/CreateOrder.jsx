import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import { toast } from 'react-toastify';

const CreateOrder = () => {
    const [inventory, setInventory] = useState([]);
    const [cart, setCart] = useState([]);
    const [selectedItemId, setSelectedItemId] = useState('');
    const [quantity, setQuantity] = useState(1);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchInventory = async () => {
            try {
                const response = await api.get('/inventory');
                setInventory(response.data);
            } catch (error) {
                toast.error('Failed to load inventory');
            }
        };
        fetchInventory();
    }, []);

    const addToCart = () => {
        if (!selectedItemId) return;
        const item = inventory.find(i => i.id === parseInt(selectedItemId));
        if (!item) return;

        if (quantity > item.quantity) {
            toast.warning(`Only ${item.quantity} available`);
            return;
        }

        const existingItem = cart.find(i => i.inventory_item_id === item.id);
        if (existingItem) {
            setCart(cart.map(i => i.inventory_item_id === item.id ? { ...i, quantity: i.quantity + quantity } : i));
        } else {
            setCart([...cart, { inventory_item_id: item.id, name: item.name, quantity }]);
        }

        // Reset selection
        setSelectedItemId('');
        setQuantity(1);
    };

    const removeFromCart = (id) => {
        setCart(cart.filter(item => item.inventory_item_id !== id));
    };

    const handleSubmit = async () => {
        if (cart.length === 0) {
            toast.error('Cart is empty');
            return;
        }

        try {
            const payload = {
                items: cart.map(({ inventory_item_id, quantity }) => ({
                    inventory_item_id,
                    quantity
                }))
            };
            await api.post('/orders', payload);
            toast.success('Order created successfully');
            navigate('/orders');
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to create order');
        }
    };

    return (
        <div style={{ maxWidth: '800px', margin: '2rem auto' }}>
            <h1 style={{ marginBottom: '2rem' }}>Create New Order</h1>

            <div className="card" style={{ marginBottom: '2rem' }}>
                <h3>Add Items</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr auto', gap: '1rem', alignItems: 'end' }}>
                    <div>
                        <label>Select Item</label>
                        <select
                            value={selectedItemId}
                            onChange={(e) => setSelectedItemId(e.target.value)}
                            style={{ marginBottom: 0 }}
                        >
                            <option value="">-- Choose Item --</option>
                            {inventory.map(item => (
                                <option key={item.id} value={item.id} disabled={item.quantity === 0}>
                                    {item.name} ({item.quantity} avail)
                                </option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label>Quantity</label>
                        <input
                            type="number"
                            min="1"
                            value={quantity}
                            onChange={(e) => setQuantity(parseInt(e.target.value))}
                            style={{ marginBottom: 0 }}
                        />
                    </div>
                    <button className="btn btn-primary" onClick={addToCart} disabled={!selectedItemId}>
                        Add
                    </button>
                </div>
            </div>

            <div className="card">
                <h3>Order Summary</h3>
                {cart.length === 0 ? (
                    <p style={{ color: 'var(--text-muted)' }}>No items selected</p>
                ) : (
                    <table style={{ marginBottom: '2rem' }}>
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Quantity</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {cart.map(item => (
                                <tr key={item.inventory_item_id}>
                                    <td>{item.name}</td>
                                    <td>{item.quantity}</td>
                                    <td>
                                        <button className="btn btn-danger" onClick={() => removeFromCart(item.inventory_item_id)}>Remove</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}

                {cart.length > 0 && (
                    <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleSubmit}>
                        Submit Order
                    </button>
                )}
            </div>
        </div>
    );
};

export default CreateOrder;
