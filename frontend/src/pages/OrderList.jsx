import React, { useEffect, useState } from 'react';
import api from '../api/client';
import { toast } from 'react-toastify';

const OrderList = () => {
    const [orders, setOrders] = useState([]);

    const fetchOrders = async () => {
        try {
            const response = await api.get('/orders');
            setOrders(response.data);
        } catch (error) {
            toast.error('Failed to fetch orders');
        }
    };

    useEffect(() => {
        fetchOrders();
    }, []);

    const handleCancel = async (orderId) => {
        if (!window.confirm('Are you sure you want to cancel this order? Stock will be restored.')) return;
        try {
            await api.post(`/orders/${orderId}/cancel`);
            toast.success('Order cancelled');
            fetchOrders();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to cancel order');
        }
    };

    return (
        <div>
            <h1 style={{ marginTop: '2rem', marginBottom: '2rem' }}>My Orders</h1>
            <div className="card table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Order ID</th>
                            <th>Date</th>
                            <th>Total Amount</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {orders.map((order) => (
                            <tr key={order.id}>
                                <td>#{order.id}</td>
                                <td>{new Date(order.created_at).toLocaleDateString()}</td>
                                <td>${order.total_amount.toFixed(2)}</td>
                                <td>
                                    <span className={`badge badge-${order.status.toLowerCase()}`}>
                                        {order.status}
                                    </span>
                                </td>
                                <td>
                                    {order.status !== 'CANCELLED' && (
                                        <button
                                            className="btn btn-danger"
                                            style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
                                            onClick={() => handleCancel(order.id)}
                                        >
                                            Cancel
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                        {orders.length === 0 && (
                            <tr>
                                <td colSpan="5" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>No orders found.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default OrderList;
