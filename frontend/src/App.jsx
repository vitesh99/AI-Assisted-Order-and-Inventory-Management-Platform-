import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect } from 'react';
import axios from 'axios';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Orders from './pages/Orders';
import Sidebar from './components/Sidebar';
import AIChat from './components/AIChat';
import WebSocketAlerts from './components/WebSocketAlerts';
import ProtectedRoute from './components/ProtectedRoute'; // Reusing this is fine
import Suppliers from './pages/Suppliers'; // Added import

const AppLayout = ({ children }) => {
    return (
        <div className="flex min-h-screen bg-gray-50 font-sans text-slate-800">
            <Sidebar />
            <WebSocketAlerts />
            <main className="flex-1 ml-64 p-8 overflow-y-auto h-screen">
                <div className="max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
            <AIChat />
        </div>
    );
};

const App = () => {
    // Global Axios Interceptor for 401s
    useEffect(() => {
        const interceptor = axios.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response && error.response.status === 401) {
                    console.log("Session expired or invalid token. Redirecting to login...");
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                }
                return Promise.reject(error);
            }
        );

        return () => {
            axios.interceptors.response.eject(interceptor);
        };
    }, []);

    return (
        <Router>
            <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<Login />} />

                {/* Protected Routes with Sidebar Layout */}
                <Route element={<ProtectedRoute />}>
                    <Route path="/dashboard" element={<AppLayout><Dashboard /></AppLayout>} />
                    <Route path="/products" element={<AppLayout><Products /></AppLayout>} />
                    <Route path="/orders" element={<AppLayout><Orders /></AppLayout>} />
                    <Route path="/suppliers" element={<AppLayout><Suppliers /></AppLayout>} />
                </Route>

                {/* Redirects */}
                <Route path="/" element={<Navigate to="/dashboard" />} />
                <Route path="*" element={<Navigate to="/dashboard" />} />
            </Routes>
        </Router>
    );
};

export default App;
