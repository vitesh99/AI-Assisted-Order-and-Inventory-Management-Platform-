import { useState, useEffect } from 'react';
import axios from 'axios';
import { Plus, Search, Truck, Phone, Mail } from 'lucide-react';

const Suppliers = () => {
    const [suppliers, setSuppliers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newSupplier, setNewSupplier] = useState({ name: '', contact_email: '', phone: '' });

    useEffect(() => {
        fetchSuppliers();
    }, []);

    const fetchSuppliers = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('/api/v1/suppliers/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setSuppliers(response.data);
        } catch (error) {
            console.error("Error fetching suppliers", error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('token');
            await axios.post('/api/v1/suppliers/', newSupplier, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setIsModalOpen(false);
            setNewSupplier({ name: '', contact_email: '', phone: '' });
            fetchSuppliers();
        } catch (error) {
            alert('Failed to create supplier');
        }
    };

    if (loading) return <div className="p-8">Loading Suppliers...</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-800">Supplier Management</h1>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="bg-indigo-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-indigo-700 transition-colors"
                >
                    <Plus size={20} />
                    Add Supplier
                </button>
            </div>

            {/* List */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {suppliers.map((supplier) => (
                    <div key={supplier.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between">
                            <div className="flex items-center gap-3">
                                <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
                                    <Truck size={24} />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-gray-900">{supplier.name}</h3>
                                    <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full">
                                        {supplier.on_time_delivery_rate}% On-Time
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div className="mt-4 space-y-2">
                            {supplier.contact_email && (
                                <div className="flex items-center gap-2 text-sm text-gray-600">
                                    <Mail size={16} />
                                    <span>{supplier.contact_email}</span>
                                </div>
                            )}
                            {supplier.phone && (
                                <div className="flex items-center gap-2 text-sm text-gray-600">
                                    <Phone size={16} />
                                    <span>{supplier.phone}</span>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl p-6 w-96 shadow-2xl">
                        <h2 className="text-xl font-bold mb-4">Add New Supplier</h2>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                                <input
                                    type="text"
                                    required
                                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                                    value={newSupplier.name}
                                    onChange={e => setNewSupplier({ ...newSupplier, name: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                <input
                                    type="email"
                                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                                    value={newSupplier.contact_email}
                                    onChange={e => setNewSupplier({ ...newSupplier, contact_email: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                                <input
                                    type="tel"
                                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                                    value={newSupplier.phone}
                                    onChange={e => setNewSupplier({ ...newSupplier, phone: e.target.value })}
                                />
                            </div>
                            <div className="flex justify-end gap-2 mt-6">
                                <button
                                    type="button"
                                    onClick={() => setIsModalOpen(false)}
                                    className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                                >
                                    Create
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Suppliers;
