import { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { IndianRupee, ShoppingBag, AlertTriangle, Package } from 'lucide-react';

const Dashboard = () => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('/api/v1/analytics/dashboard', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setStats(response.data);
        } catch (error) {
            console.error("Dashboard Error:", error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="p-8">Loading Dashboard...</div>;
    if (!stats) return <div className="p-8">Failed to load dashboard data.</div>;

    const { stats: metrics, daily_revenue, order_status_distribution } = stats;

    // Prepare chart data
    const revenueData = Object.entries(daily_revenue).map(([name, value]) => ({ name, value }));
    const pieData = Object.entries(order_status_distribution).map(([name, value]) => ({ name, value }));

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

    return (
        <div className="space-y-8">
            <h1 className="text-2xl font-bold text-gray-800">Business Overview</h1>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard title="Total Revenue" value={`₹${metrics.total_revenue.toLocaleString()}`} icon={IndianRupee} color="blue" />
                <KPICard title="Total Orders" value={metrics.total_orders} icon={ShoppingBag} color="indigo" />
                <KPICard title="Pending Orders" value={metrics.pending_orders} icon={Package} color="yellow" />
                <KPICard title="Low Stock Items" value={metrics.low_stock_count} icon={AlertTriangle} color="red" alert={metrics.low_stock_count > 0} />
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Revenue Chart */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <h3 className="text-lg font-semibold mb-4 text-gray-700">Weekly Revenue</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={revenueData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} />
                                <YAxis axisLine={false} tickLine={false} tickFormatter={(val) => `₹${val}`} />
                                <Tooltip formatter={(val) => `₹${val}`} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                                <Bar dataKey="value" fill="#4F46E5" radius={[4, 4, 0, 0]} barSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Status Distribution */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <h3 className="text-lg font-semibold mb-4 text-gray-700">Order Status</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {pieData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Top Products Table */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-100">
                    <h3 className="text-lg font-semibold text-gray-700">Top Selling Products</h3>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 text-gray-500 text-sm">
                            <tr>
                                <th className="px-6 py-3 text-left font-medium">Product Name</th>
                                <th className="px-6 py-3 text-right font-medium">Total Sold</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {stats.top_selling_products.map((product) => (
                                <tr key={product.id} className="hover:bg-gray-50/50">
                                    <td className="px-6 py-4 text-gray-800">{product.name}</td>
                                    <td className="px-6 py-4 text-right font-medium text-gray-600">{product.total_sold} units</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

const KPICard = ({ title, value, icon: Icon, color, alert }) => {
    const colorClasses = {
        blue: 'bg-blue-50 text-blue-600',
        indigo: 'bg-indigo-50 text-indigo-600',
        yellow: 'bg-yellow-50 text-yellow-600',
        red: 'bg-red-50 text-red-600',
    };

    return (
        <div className={`bg-white p-6 rounded-xl shadow-sm border ${alert ? 'border-red-200 ring-2 ring-red-50' : 'border-gray-100'}`}>
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm font-medium text-gray-500">{title}</p>
                    <p className="text-2xl font-bold mt-1 text-gray-900">{value}</p>
                </div>
                <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
                    <Icon size={24} />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
