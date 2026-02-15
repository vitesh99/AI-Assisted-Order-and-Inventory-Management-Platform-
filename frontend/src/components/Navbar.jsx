import { Link, useNavigate, useLocation } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();
    const location = useLocation(); // Triggers re-render on route change
    const token = localStorage.getItem('token');

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <nav className="bg-white shadow">
            <div className="container mx-auto px-4">
                <div className="flex justify-between h-16">
                    <div className="flex items-center">
                        <Link to="/" className="text-xl font-bold text-blue-600">AI Inventory</Link>
                        {token && (
                            <div className="ml-10 flex items-baseline space-x-4">
                                <Link to="/products" className={`px-3 py-2 rounded-md ${location.pathname === '/products' ? 'text-blue-600 font-medium' : 'text-gray-600 hover:text-gray-900'}`}>Products</Link>
                                <Link to="/orders" className={`px-3 py-2 rounded-md ${location.pathname === '/orders' ? 'text-blue-600 font-medium' : 'text-gray-600 hover:text-gray-900'}`}>Orders</Link>
                            </div>
                        )}
                    </div>
                    <div className="flex items-center">
                        {token ? (
                            <button
                                onClick={handleLogout}
                                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md"
                            >
                                Logout
                            </button>
                        ) : (
                            <Link to="/login" className="text-blue-600 hover:text-blue-800 px-3 py-2 rounded-md">Login</Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
