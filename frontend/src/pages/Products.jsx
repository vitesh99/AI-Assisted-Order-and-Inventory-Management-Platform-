import { useState, useEffect } from 'react';
import axios from 'axios';
import { Package, AlertTriangle, CheckCircle } from 'lucide-react';

const Products = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchProducts();
    }, []);

    const fetchProducts = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('/api/v1/inventory/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setProducts(response.data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="p-8">Loading Inventory...</div>;

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-800">Inventory Management</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map(product => {
                    const lowStock = product.stock_quantity < 10;
                    return (
                        <div key={product.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all group">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-3 bg-blue-50 text-blue-600 rounded-lg group-hover:bg-blue-600 group-hover:text-white transition-colors">
                                    <Package size={24} />
                                </div>
                                <span className="text-lg font-bold text-gray-900">₹{product.price}</span>
                            </div>

                            <h3 className="text-xl font-semibold mb-2 text-gray-800">{product.name}</h3>
                            <p className="text-gray-500 text-sm mb-4 line-clamp-2">{product.description}</p>

                            <div className="flex justify-between items-center pt-4 border-t border-gray-50">
                                <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${lowStock ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'
                                    }`}>
                                    {lowStock ? <AlertTriangle size={14} /> : <CheckCircle size={14} />}
                                    <span>Stock: {product.stock_quantity}</span>
                                </div>
                                {product.supplier && (
                                    <span className="text-xs text-gray-400">
                                        {product.supplier.name}
                                    </span>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Products;
