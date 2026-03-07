import React, { useState, useEffect } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    PieChart, Pie, Cell, Legend
} from 'recharts';
import { TrendingUp, AlertCircle, FileText, Package, ShoppingCart, Activity } from 'lucide-react';
import { formatPKR } from '../../utils/currency';
import api from '../../services/api';

const COLORS = ['#0ea5e9', '#8b5cf6', '#10b981', '#f59e0b'];

const Dashboard = () => {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState({
        kpis: null,
        monthlyRevenue: [],
        topProducts: [],
        recentSales: [],
        lowStock: []
    });

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                // Attempt to fetch from real API
                const [kpisRes, revenueRes, productsRes, salesRes, stockRes] = await Promise.all([
                    api.get('dashboard/kpis/'),
                    api.get('dashboard/monthly-revenue/'),
                    api.get('dashboard/top-products/'),
                    api.get('dashboard/recent-sales/'),
                    api.get('dashboard/low-stock-products/')
                ]);

                setData({
                    kpis: kpisRes.data,
                    monthlyRevenue: revenueRes.data,
                    topProducts: productsRes.data,
                    recentSales: salesRes.data,
                    lowStock: stockRes.data
                });
            } catch (error) {
                console.warn('Backend API failed, using mock data for Dashboard layout');

                // Fallback Mock Data for UI demonstration
                setData({
                    kpis: {
                        total_products: 342,
                        total_inventory_value: 1250000,
                        total_revenue: 845000,
                        total_purchases_value: 420000,
                        total_invoices: 156,
                        unpaid_invoices: 23,
                        low_stock_count: 12,
                        // Fallbacks for the Phase 1 UI cards
                        cash_balance: 85450,
                        ar_balance: 32100
                    },
                    monthlyRevenue: [
                        { month: 'Jan', revenue: 120000 },
                        { month: 'Feb', revenue: 150000 },
                        { month: 'Mar', revenue: 180000 },
                        { month: 'Apr', revenue: 140000 },
                        { month: 'May', revenue: 210000 },
                        { month: 'Jun', revenue: 250000 },
                    ],
                    topProducts: [
                        { product_name: 'A4 Copy Paper', quantity_sold: 500, total_revenue: 25000 },
                        { product_name: 'Office Chair Exec', quantity_sold: 150, total_revenue: 45000 },
                        { product_name: 'Wireless Mouse', quantity_sold: 300, total_revenue: 15000 },
                        { product_name: 'Stapler Pro', quantity_sold: 450, total_revenue: 4500 },
                    ],
                    recentSales: [
                        { sale_id: 101, product_name: 'A4 Copy Paper', customer_name: 'Acme Corp', quantity_sold: 50, total_price: 2500, sale_date: '2023-10-25' },
                        { sale_id: 102, product_name: 'Office Chair Exec', customer_name: 'Innovate Ltd', quantity_sold: 10, total_price: 3000, sale_date: '2023-10-24' },
                        { sale_id: 103, product_name: 'Wireless Mouse', customer_name: 'Tech Solutions', quantity_sold: 25, total_price: 1250, sale_date: '2023-10-23' },
                    ],
                    lowStock: [
                        { product_id: 5, product_name: 'Printer Ink Black', sku: 'INK-BLK-01', stock_quantity: 5, reorder_level: 20, unit_price: 1500 },
                        { product_id: 12, product_name: 'Notepads A5', sku: 'PAD-A5-10', stock_quantity: 12, reorder_level: 50, unit_price: 100 },
                    ]
                });
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, []);

    if (loading) {
        return <div className="min-h-[60vh] flex items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>;
    }

    const { kpis, monthlyRevenue, topProducts, recentSales, lowStock } = data;

    return (
        <div className="space-y-6">
            {/* Top Value Cards (Mixed from Phase 1 UI & New API Data) */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Cash Balance / Total Revenue */}
                <div className="bg-surface rounded-3xl p-6 border border-gray-100 shadow-sm flex flex-col hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                        <h3 className="text-textMuted font-semibold text-sm">Total Revenue</h3>
                        <div className="p-2 bg-green-100 rounded-lg text-success"><Activity className="w-5 h-5" /></div>
                    </div>
                    <p className="text-3xl font-bold text-textMain mb-4">{formatPKR(kpis.cash_balance || kpis.total_revenue)}</p>
                    <div className="flex items-center text-sm">
                        <span className="text-success font-semibold flex items-center">
                            <TrendingUp className="w-4 h-4 mr-1" /> +12.5%
                        </span>
                        <span className="text-gray-400 ml-2">vs last month</span>
                    </div>
                </div>

                {/* Accounts Rec / Purchases */}
                <div className="bg-surface rounded-3xl p-6 border border-gray-100 shadow-sm flex flex-col hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                        <h3 className="text-textMuted font-semibold text-sm">Target vs Actual</h3>
                        <div className="p-2 bg-red-100 rounded-lg text-danger"><AlertCircle className="w-5 h-5" /></div>
                    </div>
                    <p className="text-3xl font-bold text-textMain mb-4">{formatPKR(kpis.ar_balance || kpis.total_purchases_value)}</p>
                    <div className="flex items-center text-sm font-medium">
                        <span className="text-danger flex items-center">
                            <TrendingUp className="w-4 h-4 mr-1 rotate-180" /> -4.2%
                        </span>
                        <span className="text-gray-400 ml-2">vs last month</span>
                    </div>
                </div>

                {/* Total Products */}
                <div className="bg-surface rounded-3xl p-6 border border-gray-100 shadow-sm flex flex-col hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                        <h3 className="text-textMuted font-semibold text-sm">Net Profit</h3>
                        <div className="p-2 bg-sky-100 rounded-lg text-primary"><Package className="w-5 h-5" /></div>
                    </div>
                    <p className="text-3xl font-bold text-textMain mb-4">{formatPKR(750000)}</p>
                    <div className="flex items-center text-sm font-medium">
                        <span className="text-success flex items-center">
                            <TrendingUp className="w-4 h-4 mr-1" /> +18.1%
                        </span>
                        <span className="text-gray-400 ml-2">vs last month</span>
                    </div>
                </div>

                {/* Inventory Value */}
                <div className="bg-surface rounded-3xl p-6 border border-gray-100 shadow-sm flex flex-col hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                        <h3 className="text-textMuted font-semibold text-sm">Cash Flow</h3>
                        <div className="p-2 bg-purple-100 rounded-lg text-purple-600"><ShoppingCart className="w-5 h-5" /></div>
                    </div>
                    <p className="text-3xl font-bold text-textMain mb-4">{formatPKR(300000)}</p>
                    <div className="flex items-center text-sm font-medium">
                        <span className="text-danger flex items-center">
                            <TrendingUp className="w-4 h-4 mr-1 rotate-180" /> -2.5%
                        </span>
                        <span className="text-gray-400 ml-2">vs last month</span>
                    </div>
                </div>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Revenue Chart */}
                <div className="bg-surface rounded-3xl p-6 border border-gray-100 shadow-sm">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-lg font-bold text-textMain">Income vs Expense Trends</h3>
                        <div className="flex space-x-4 text-sm">
                            <div className="flex items-center"><span className="w-2.5 h-2.5 rounded-full bg-primary mr-2"></span>Income</div>
                            <div className="flex items-center"><span className="w-2.5 h-2.5 rounded-full bg-gray-200 mr-2"></span>Expenses</div>
                        </div>
                    </div>
                    <div className="h-72 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={monthlyRevenue} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                                <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 500 }} dy={10} />
                                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 500 }} tickFormatter={(val) => `Rs ${val / 1000}k`} />
                                <Tooltip
                                    cursor={{ fill: '#f8fafc' }}
                                    contentStyle={{ borderRadius: '16px', border: '1px solid #f1f5f9', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                                    formatter={(value) => [formatPKR(value), "Revenue"]}
                                />
                                <Bar dataKey="revenue" fill="#0ea5e9" radius={[6, 6, 0, 0]} maxBarSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Top Products Pie Chart */}
                <div className="bg-surface rounded-3xl p-6 border border-gray-100 shadow-sm">
                    <h3 className="text-lg font-bold text-textMain mb-6">Top Selling Categories</h3>
                    <div className="h-72 w-full flex items-center justify-center relative">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={topProducts}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={90}
                                    outerRadius={120}
                                    paddingAngle={2}
                                    dataKey="total_revenue"
                                    nameKey="product_name"
                                    stroke="none"
                                >
                                    {topProducts.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    formatter={(value) => [formatPKR(value), "Revenue"]}
                                    contentStyle={{ borderRadius: '16px', border: '1px solid #f1f5f9', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                                />
                                <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px', fontWeight: 500, color: '#64748b' }} />
                            </PieChart>
                        </ResponsiveContainer>
                        {/* Center Text */}
                        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none -mt-8">
                            <span className="text-xs text-textMuted font-bold uppercase tracking-wider">Total Sales</span>
                            <span className="text-xl font-extrabold text-textMain mt-1">
                                {formatPKR(topProducts.reduce((acc, curr) => acc + parseFloat(curr.total_revenue), 0))}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Tables Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Recent Sales Table */}
                <div className="bg-surface rounded-3xl border border-gray-100 shadow-sm overflow-hidden flex flex-col">
                    <div className="p-6 border-b border-gray-50 flex justify-between items-center">
                        <h3 className="text-lg font-bold text-textMain">Recent Sales</h3>
                        <button className="text-sm font-semibold text-primary hover:text-primaryDark">View All</button>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-white text-textMuted text-xs uppercase tracking-wider">
                                <tr>
                                    <th className="px-6 py-4 font-semibold">Product</th>
                                    <th className="px-6 py-4 font-semibold">Customer</th>
                                    <th className="px-6 py-4 font-semibold">Amount</th>
                                    <th className="px-6 py-4 font-semibold">Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                {recentSales.map((sale) => (
                                    <tr key={sale.sale_id} className="border-b border-gray-50 hover:bg-slate-50 transition-colors">
                                        <td className="px-6 py-4 font-semibold text-textMain">{sale.product_name}</td>
                                        <td className="px-6 py-4 text-textMuted">{sale.customer_name}</td>
                                        <td className="px-6 py-4 font-bold text-textMain">{formatPKR(sale.total_price)}</td>
                                        <td className="px-6 py-4 text-textMuted">{sale.sale_date}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Low Stock Alerts */}
                <div className="bg-surface rounded-3xl border border-gray-100 shadow-sm overflow-hidden flex flex-col">
                    <div className="p-6 border-b border-gray-50">
                        <h3 className="text-lg font-bold text-textMain flex items-center">
                            <AlertCircle className="w-5 h-5 mr-2 text-danger" /> Low Stock Alerts
                        </h3>
                    </div>
                    <div className="overflow-x-auto flex-1">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-white text-textMuted text-xs uppercase tracking-wider">
                                <tr>
                                    <th className="px-6 py-4 font-semibold">Product / SKU</th>
                                    <th className="px-6 py-4 font-semibold">Current Stock</th>
                                    <th className="px-6 py-4 font-semibold">Reorder Lvl</th>
                                    <th className="px-6 py-4 font-semibold">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {lowStock.map((item) => (
                                    <tr key={item.product_id} className="border-b border-gray-50 hover:bg-slate-50 transition-colors">
                                        <td className="px-6 py-4">
                                            <p className="font-semibold text-textMain">{item.product_name}</p>
                                            <p className="text-xs text-textMuted mt-0.5">{item.sku}</p>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-bold bg-red-50 text-danger border border-red-100">
                                                {item.stock_quantity}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-textMuted font-medium">{item.reorder_level}</td>
                                        <td className="px-6 py-4">
                                            <button className="text-sm font-semibold text-primary hover:text-primaryDark hover:underline">
                                                Restock
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                                {lowStock.length === 0 && (
                                    <tr>
                                        <td colSpan="4" className="px-6 py-8 text-center text-textMuted">
                                            Inventory looks healthy! No low stock alerts.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Dashboard;
