import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import { toast } from 'react-toastify';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        try {
            const response = await api.post('/auth/login', formData);
            login(response.data.access_token);
            toast.success('Logged in successfully');
            navigate('/');
        } catch (error) {
            toast.error('Login failed. Please check your credentials.');
        }
    };

    return (
        <div className="auth-form card">
            <h2 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>Welcome Back</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        placeholder="admin@example.com"
                    />
                </div>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>Login</button>
            </form>
            <div style={{ marginTop: '1rem', textAlign: 'center', fontSize: '0.875rem' }}>
                <p style={{ color: 'var(--text-muted)' }}>Demo Account: admin@example.com / password</p>
            </div>
        </div>
    );
};

export default Login;
