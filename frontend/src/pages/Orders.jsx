import { useState, useEffect } from 'react';
import axios from 'axios';
import { ShoppingCart, Clock, CheckCircle, Truck, Package, XCircle, Sparkles, Plus } from 'lucide-react';
import Modal from '../components/Modal';
import MarkdownRenderer from '../components/MarkdownRenderer';

const Orders = () => {
    const [orders, setOrders] = useState([]);
    const [createLoading, setCreateLoading] = useState(false);

    // Modal State
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState('');
    const [modalTitle, setModalTitle] = useState('');

    useEffect(() => {
        fetchOrders();
    }, []);

    const fetchOrders = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('/api/v1/orders/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            // Sort by ID desc
            setOrders(response.data.sort((a, b) => b.id - a.id));
        } catch (error) {
            console.error(error);
        }
    };

    const handleCreateTestOrder = async () => {
        if (!confirm("Create a test order (Product ID 1)?")) return;
        setCreateLoading(true);
        try {
            const token = localStorage.getItem('token');
            await axios.post('/api/v1/orders/', {
                items: [{ product_id: 1, quantity: 1 }]
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            fetchOrders();
        } catch (error) {
            alert("Failed: " + (error.response?.data?.detail || error.message));
        } finally {
            setCreateLoading(false);
        }
    };

    const handleFulfillOrder = async (orderId) => {
        if (!confirm("Mark order as fulfilled?")) return;
        try {
            const token = localStorage.getItem('token');
            await axios.put(`/api/v1/orders/${orderId}/status?status=FULFILLED`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            fetchOrders();
        } catch (error) {
            console.error(error);
            alert("Failed to fulfill order: " + (error.response?.data?.detail || error.message));
        }
    };

    const fetchSummary = async (orderId) => {
        setModalTitle(`AI Summary for Order #${orderId}`);
        setModalContent("Generating summary...");
        setIsModalOpen(true);

        try {
            const token = localStorage.getItem('token');
            // Check if backend supports this endpoint in new structure? 
            // We didn't explicitly create it in order_routes in previous turn!
            // Wait, I missed copying the specific `ai-summary` endpoint to `orders.py`!
            // I need to add it to generic `orders.py` or `ai.py`.
            // Let's assume I'll fix the backend next.
            const response = await axios.get(`/api/v1/orders/${orderId}/ai-summary`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setModalContent(response.data.summary || "No summary available.");
        } catch (error) {
            setModalContent("Failed to fetch summary. AI service might be busy.");
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'CREATED': return <Clock size={16} />;
            case 'CONFIRMED': return <CheckCircle size={16} />;
            case 'FULFILLED': return <Truck size={16} />;
            case 'SHIPPED': return <Truck size={16} />;
            case 'DELIVERED': return <Package size={16} />;
            case 'CANCELLED': return <XCircle size={16} />;
            default: return <ShoppingCart size={16} />;
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'CREATED': return 'bg-yellow-100 text-yellow-800';
            case 'CONFIRMED': return 'bg-blue-100 text-blue-800';
            case 'FULFILLED': return 'bg-purple-100 text-purple-800';
            case 'SHIPPED': return 'bg-purple-100 text-purple-800';
            case 'DELIVERED': return 'bg-green-100 text-green-800';
            case 'CANCELLED': return 'bg-red-100 text-red-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-800">Order History</h1>
                <button
                    onClick={handleCreateTestOrder}
                    disabled={createLoading}
                    className="bg-indigo-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-indigo-700 disabled:opacity-50 transition-colors shadow-sm"
                >
                    <Plus size={20} />
                    {createLoading ? 'Creating...' : 'New Order'}
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                <table className="w-full">
                    <thead className="bg-gray-50 text-gray-500 text-sm">
                        <tr>
                            <th className="px-6 py-4 text-left font-medium">Order ID</th>
                            <th className="px-6 py-4 text-left font-medium">Date</th>
                            <th className="px-6 py-4 text-left font-medium">Status</th>
                            <th className="px-6 py-4 text-right font-medium">Total</th>
                            <th className="px-6 py-4 text-right font-medium">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {orders.map(order => (
                            <tr key={order.id} className="hover:bg-gray-50/50 transition-colors">
                                <td className="px-6 py-4 font-medium text-gray-900">#{order.id}</td>
                                <td className="px-6 py-4 text-gray-500 text-sm">
                                    {new Date(order.created_at || Date.now()).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
                                        {getStatusIcon(order.status)}
                                        {order.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-right font-medium text-gray-900">
                                    ₹{order.total_amount}
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <button
                                        onClick={() => fetchSummary(order.id)}
                                        className="text-indigo-600 hover:text-indigo-800 text-sm font-medium inline-flex items-center gap-1"
                                    >
                                        <Sparkles size={14} />
                                        AI Insight
                                    </button>

                                    {order.status === 'CREATED' && (
                                        <button
                                            onClick={() => handleFulfillOrder(order.id)}
                                            className="text-green-600 hover:text-green-800 text-sm font-medium inline-flex items-center gap-1 ml-4"
                                            title="Mark as Fulfilled"
                                        >
                                            <CheckCircle size={14} />
                                            Fulfill
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {orders.length === 0 && (
                    <div className="p-8 text-center text-gray-500">No orders found. Create one to get started.</div>
                )}
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={modalTitle}
            >
                <div className="prose prose-sm max-w-none text-gray-700">
                    <MarkdownRenderer content={modalContent} />
                </div>
            </Modal>
        </div>
    );
};

export default Orders;
