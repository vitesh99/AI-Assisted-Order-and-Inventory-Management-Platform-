import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import InventoryList from './pages/InventoryList';
import OrderList from './pages/OrderList';
import CreateOrder from './pages/CreateOrder';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const PrivateRoute = ({ children }) => {
    const { token } = useAuth();
    return token ? children : <Navigate to="/login" />;
};

const NavBar = () => {
    const { token, logout } = useAuth();
    if (!token) return null;

    return (
        <nav className="nav">
            <div className="container nav-content">
                <div style={{ fontWeight: 'bold', fontSize: '1.25rem' }}>AI Inventory</div>
                <div className="nav-links">
                    <Link to="/">Inventory</Link>
                    <Link to="/orders">Orders</Link>
                    <Link to="/create-order">New Order</Link>
                    <a href="#" onClick={(e) => { e.preventDefault(); logout(); }}>Logout</a>
                </div>
            </div>
        </nav>
    );
};

function App() {
    return (
        <AuthProvider>
            <Router>
                <NavBar />
                <div className="container">
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/" element={
                            <PrivateRoute>
                                <InventoryList />
                            </PrivateRoute>
                        } />
                        <Route path="/orders" element={
                            <PrivateRoute>
                                <OrderList />
                            </PrivateRoute>
                        } />
                        <Route path="/create-order" element={
                            <PrivateRoute>
                                <CreateOrder />
                            </PrivateRoute>
                        } />
                    </Routes>
                </div>
                <ToastContainer position="bottom-right" theme="dark" />
            </Router>
        </AuthProvider>
    );
}

export default App;
