import React, { useState, useEffect } from 'react';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { formatPKR } from '../../utils/currency';
import api from '../../services/api';
import { useNavigate } from 'react-router-dom';
import { Wallet, Laptop, Smartphone, Printer, Receipt } from 'lucide-react';

const Dashboard = () => {
    const navigate = useNavigate();
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
                console.warn('Backend API failed, using mock data for AI Dashboard layout');

                setData({
                    kpis: {
                        total_revenue: 345670500,
                        account_balance: 84200000,
                        inventory_value: 12450000,
                        total_products: 340,
                        unpaid_invoices_amount: 4235000,
                        unpaid_invoices_count: 12
                    },
                    monthlyRevenue: [
                        { month: 'JUL', revenue: 120000 },
                        { month: 'AUG', revenue: 150000 },
                        { month: 'SEP', revenue: 130000 },
                        { month: 'OCT', revenue: 180000 },
                        { month: 'NOV', revenue: 160000 },
                        { month: 'DEC', revenue: 210000 },
                    ],
                    topProducts: [
                        { product_name: 'A4 Copy Paper', quantity_sold: 500, total_revenue: 25000 },
                    ],
                    recentSales: [
                        { sale_id: 982, invoice_number: 'INV-0982', total_price: 45000, sale_date: 'Oct 24' },
                        { sale_id: 983, invoice_number: 'INV-0983', total_price: 128000, sale_date: 'Oct 22' },
                        { sale_id: 984, invoice_number: 'INV-0984', total_price: 72000, sale_date: 'Oct 19' },
                    ],
                    lowStock: [
                        { product_id: 5, product_name: 'Laptops', sku: 'TECH-LAP-01', stock_quantity: 84, inventory_value: 8400000 },
                        { product_id: 12, product_name: 'Smartphones', sku: 'TECH-PHN-02', stock_quantity: 12, inventory_value: 1200000, isReorder: true },
                        { product_id: 15, product_name: 'Supplies', sku: 'OFF-SUP-01', stock_quantity: 244, inventory_value: 400000 },
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

    const { kpis, monthlyRevenue, recentSales, lowStock } = data;

    // Custom Tooltip for Area Chart
    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-lg text-sm">
                    <p className="font-bold text-textMain mb-1">{label}</p>
                    <p className="font-semibold text-primary">
                        {formatPKR(payload[0].value)}
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="space-y-8">
            {/* Header/Hero Section */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-extrabold text-textMain">Business Overview</h1>
                    <p className="text-textMuted text-sm mt-1">Welcome back, Ali. Here is your current business performance summary.</p>
                </div>
            </div>

            {/* KPI 4-Card Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
                <div onClick={() => navigate('/sales')} className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative overflow-hidden group cursor-pointer hover:border-primary/30 transition-colors">
                    <div className="absolute top-0 right-0 w-16 h-16 bg-primary/5 rounded-bl-full"></div>
                    <p className="text-textMuted text-sm font-medium">Total Revenue</p>
                    <div className="flex flex-col items-start justify-between mt-3 gap-2">
                        <h3 className="text-2xl font-extrabold text-slate-900">{formatPKR(kpis.total_revenue)}</h3>
                        <span className="text-emerald-600 text-xs font-bold flex items-center justify-center bg-emerald-50 px-2 py-1 rounded-full w-max">
                            <span className="material-symbols-outlined !text-xs mr-0.5">trending_up</span>+5.2%
                        </span>
                    </div>
                </div>

                <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative overflow-hidden">
                    <p className="text-textMuted text-sm font-medium">Account Balance</p>
                    <div className="flex flex-col items-start justify-between mt-3 gap-2">
                        <h3 className="text-2xl font-extrabold text-slate-900">{formatPKR(kpis.account_balance)}</h3>
                        <span className="text-emerald-600 text-xs font-bold flex items-center justify-center bg-emerald-50 px-2 py-1 rounded-full w-max">
                            <span className="material-symbols-outlined !text-xs mr-0.5">trending_up</span>+1.1%
                        </span>
                    </div>
                </div>

                <div onClick={() => navigate('/products')} className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative overflow-hidden cursor-pointer hover:border-primary/30 transition-colors">
                    <p className="text-textMuted text-sm font-medium">Inventory Value</p>
                    <div className="flex flex-col items-start justify-between mt-3 gap-2">
                        <h3 className="text-2xl font-extrabold text-slate-900">{formatPKR(kpis.inventory_value)}</h3>
                        <span className="text-amber-600 text-xs font-bold flex items-center justify-center bg-amber-50 px-2 py-1 rounded-full w-max">
                            <span className="material-symbols-outlined !text-xs mr-0.5">inventory</span>{kpis.total_products} Items
                        </span>
                    </div>
                </div>

                <div onClick={() => navigate('/invoices')} className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative overflow-hidden cursor-pointer hover:border-primary/30 transition-colors">
                    <p className="text-textMuted text-sm font-medium">Outstanding Invoices</p>
                    <div className="flex flex-col items-start justify-between mt-3 gap-2">
                        <h3 className="text-2xl font-extrabold text-slate-900">{formatPKR(kpis.unpaid_invoices_amount)}</h3>
                        <span className="text-rose-600 text-xs font-bold flex items-center justify-center bg-rose-50 px-2 py-1 rounded-full w-max">
                            <span className="material-symbols-outlined !text-xs mr-0.5">error</span>{kpis.unpaid_invoices_count} Overdue
                        </span>
                    </div>
                </div>
            </div>

            {/* Middle Section: Chart & AI Insights */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Recharts Area Flow (Dynamic replacement for HTML SVG) */}
                <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex flex-col">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h4 className="font-bold text-lg">Sales Performance (Rs.)</h4>
                            <p className="text-textMuted text-xs">Monthly revenue and cost analysis</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-primary"></span>
                                <span className="text-[10px] text-textMuted font-bold">Revenue (Rs.)</span>
                            </div>
                            <select className="bg-slate-50 border-none rounded-lg text-xs font-bold py-1.5 px-3 outline-none">
                                <option>Last 6 Months</option>
                                <option>Last Year</option>
                            </select>
                        </div>
                    </div>

                    <div className="flex-1 w-full min-h-[250px] relative">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={monthlyRevenue} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#1392ec" stopOpacity={0.2} />
                                        <stop offset="95%" stopColor="#1392ec" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="#f0f3f4" />
                                <XAxis
                                    dataKey="month"
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#617989', fontSize: 10, fontWeight: 'bold' }}
                                    dy={10}
                                />
                                <YAxis
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#617989', fontSize: 10, fontWeight: 'bold' }}
                                    tickFormatter={(val) => `Rs ${val / 1000}k`}
                                    orientation="left"
                                />
                                <Tooltip content={<CustomTooltip />} />
                                <Area
                                    type="monotone"
                                    dataKey="revenue"
                                    stroke="#1392ec"
                                    strokeWidth={3}
                                    fillOpacity={1}
                                    fill="url(#colorRevenue)"
                                    activeDot={{ r: 6, fill: '#1392ec', stroke: '#fff', strokeWidth: 2 }}
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* AI Smart Insights */}
                <div className="bg-white p-6 rounded-xl border border-primary/20 shadow-sm flex flex-col relative overflow-hidden">
                    <div className="absolute -right-4 -top-4 w-24 h-24 ai-gradient opacity-5 rounded-full blur-2xl"></div>
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                            <div className="ai-gradient p-1.5 rounded-lg text-white flex items-center justify-center">
                                <span className="material-symbols-outlined !text-lg">auto_awesome</span>
                            </div>
                            <h4 className="font-bold text-lg text-textMain">AI Smart Insights</h4>
                        </div>
                        <span className="text-[10px] font-bold text-primary px-2 py-0.5 bg-primary/10 rounded uppercase">Live</span>
                    </div>

                    <div className="space-y-4 flex-1 mt-2">
                        <div className="flex gap-3 p-3 bg-slate-50 rounded-lg border-l-4 border-primary">
                            <span className="material-symbols-outlined text-primary !text-lg shrink-0">trending_up</span>
                            <p className="text-xs text-textMain leading-relaxed font-medium">Sales are projected to increase by <span className="text-primary font-bold">10%</span> next month based on current trends.</p>
                        </div>

                        <div className="flex gap-3 p-3 bg-slate-50 rounded-lg border-l-4 border-rose-500">
                            <span className="material-symbols-outlined text-rose-500 !text-lg shrink-0">warning</span>
                            <p className="text-xs text-textMain leading-relaxed font-medium"><span className="text-rose-500 font-bold">Low stock alert</span> for Office Supplies. Current rate of consumption exceeds supply.</p>
                        </div>

                        <div className="flex gap-3 p-3 bg-slate-50 rounded-lg border-l-4 border-emerald-500">
                            <span className="material-symbols-outlined text-emerald-500 !text-lg shrink-0">payments</span>
                            <p className="text-xs text-textMain leading-relaxed font-medium">Potential to save <span className="text-emerald-600 font-bold">Rs. 25,000</span> by switching to bulk vendor payments.</p>
                        </div>
                    </div>

                    <button 
                        onClick={() => navigate('/ai-chat')}
                        className="mt-6 w-full py-2 ai-gradient text-white rounded-lg text-xs font-bold transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg hover:shadow-primary/40"
                    >
                        Ask Bizzionary AI
                    </button>
                </div>
            </div>

            {/* Bottom 3 Widgets */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Cash Flow */}
                <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex flex-col">
                    <div className="flex items-center gap-3 justify-between mb-4">
                        <h4 className="font-bold text-lg">Cash Flow Overview</h4>
                        <Wallet className="w-5 h-5 text-textMuted" />
                    </div>

                    <div className="space-y-4 flex-1">
                        <div className="flex flex-col gap-1 w-full">
                            <div className="flex justify-between items-center text-xs font-bold w-full">
                                <span className="text-textMuted text-left">Inflow (Current Month)</span>
                                <span className="text-emerald-600 text-right">Rs. 12,450,000</span>
                            </div>
                            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                <div className="bg-emerald-500 h-full w-[75%]"></div>
                            </div>
                        </div>

                        <div className="flex flex-col gap-1 mt-4 w-full">
                            <div className="flex justify-between items-center text-xs font-bold w-full">
                                <span className="text-textMuted text-left">Outflow (Current Month)</span>
                                <span className="text-rose-600 text-right">Rs. 8,120,000</span>
                            </div>
                            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                <div className="bg-rose-500 h-full w-[45%]"></div>
                            </div>
                        </div>

                        <div className="mt-6 p-4 rounded-lg bg-slate-50 border border-slate-200">
                            <p className="text-xs text-textMuted font-medium">Net Position</p>
                            <p className="text-xl font-extrabold text-primary pt-1">Rs. 4,330,000</p>
                            <p className="text-[10px] text-emerald-600 font-bold mt-1">+12% vs last month</p>
                        </div>
                    </div>

                    <button 
                        onClick={() => navigate('/accounts')}
                        className="mt-6 w-full py-2 bg-slate-100 text-slate-700 rounded-lg text-xs font-bold transition-all duration-300 transform hover:-translate-y-1 hover:shadow-md hover:bg-slate-200"
                    >
                        Manage Accounts
                    </button>
                </div>

                {/* Inventory Summary */}
                <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm lg:col-span-1">
                    <div className="flex items-center justify-between mb-6">
                        <h4 className="font-bold text-lg">Inventory Summary</h4>
                        <div className="flex gap-2">
                            <div className="flex items-center gap-1">
                                <div className="w-2 h-2 rounded-full bg-rose-500"></div>
                                <span className="text-[10px] text-textMuted font-medium uppercase">Low</span>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-3">
                        {lowStock.map((item, idx) => (
                            <div key={idx} className="flex items-center justify-between p-3 border border-gray-100 rounded-lg">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 bg-primary/10 rounded flex flex-shrink-0 items-center justify-center text-primary">
                                        {item.product_name.includes('Lap') ? <Laptop className="w-5 h-5" /> :
                                         item.product_name.includes('Smart') ? <Smartphone className="w-5 h-5" /> : 
                                         <Printer className="w-5 h-5" />}
                                    </div>
                                    <div className="min-w-0">
                                        <p className="text-sm font-bold truncate">{item.product_name}</p>
                                        <p className="text-[10px] text-textMuted">{item.stock_quantity} Units</p>
                                    </div>
                                </div>
                                <div className="text-right flex-shrink-0 ml-2">
                                    {item.isReorder ? (
                                        <span className="text-[10px] font-bold text-rose-500 whitespace-nowrap">Reorder</span>
                                    ) : (
                                        <p className="text-sm font-bold whitespace-nowrap">{formatPKR(item.inventory_value)}</p>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Recent Activities */}
                <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
                    <div className="flex items-center justify-between mb-4">
                        <h4 className="font-bold text-lg">Recent Activities</h4>
                        <button onClick={() => navigate('/invoices')} className="text-primary text-xs font-bold hover:underline">View All</button>
                    </div>

                    <div className="space-y-4">
                        {recentSales.map((sale, idx) => (
                            <div key={idx} className={`flex items-center justify-between border-b border-slate-50 pb-2 ${idx === recentSales.length - 1 ? 'border-b-0 pb-0' : ''}`}>
                                <div className="flex items-center gap-3">
                                    <Receipt className="w-5 h-5 text-primary flex-shrink-0" />
                                    <div className="min-w-0">
                                        <p className="text-sm font-semibold truncate">{sale.invoice_number}</p>
                                        <p className="text-[10px] text-textMuted">{sale.sale_date}</p>
                                    </div>
                                </div>
                                <p className={`text-sm font-bold flex-shrink-0 ml-2 whitespace-nowrap ${idx === 1 ? 'text-amber-600' : 'text-textMain'}`}>
                                    {formatPKR(sale.total_price)}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Dashboard;
