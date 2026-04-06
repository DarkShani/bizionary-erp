import React, { useState, useEffect } from 'react';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { formatPKR } from '../../utils/currency';
import api from '../../services/api';
import { useNavigate } from 'react-router-dom';
import { Wallet, Package, AlertTriangle, Receipt } from 'lucide-react';

const Dashboard = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState({
        kpis: null,
        monthlyRevenue: [],
        outstandingInvoices: [],
        recentSales: [],
        lowStock: []
    });

    useEffect(() => {
        const normalizeKpis = (raw = {}) => ({
            total_revenue: raw.total_revenue ?? 0,
            total_purchases_value: raw.total_purchases_value ?? 0,
            inventory_value: raw.total_inventory_value ?? 0,
            total_products: raw.total_products ?? 0,
            unpaid_invoices_count: raw.unpaid_invoices ?? 0,
            low_stock_count: raw.low_stock_count ?? 0,
            total_invoices: raw.total_invoices ?? 0,
        });

        const fetchDashboardData = async () => {
            try {
                const [kpisRes, revenueRes, salesRes, stockRes, outstandingRes] = await Promise.allSettled([
                    api.get('dashboard/kpis/'),
                    api.get('dashboard/monthly-revenue/'),
                    api.get('dashboard/recent-sales/'),
                    api.get('dashboard/low-stock-products/'),
                    api.get('dashboard/outstanding-invoices/')
                ]);

                const endpointResults = [
                    ['dashboard/kpis/', kpisRes],
                    ['dashboard/monthly-revenue/', revenueRes],
                    ['dashboard/recent-sales/', salesRes],
                    ['dashboard/low-stock-products/', stockRes],
                    ['dashboard/outstanding-invoices/', outstandingRes],
                ];

                const outstandingInvoices = outstandingRes.status === 'fulfilled' ? outstandingRes.value.data : [];
                const unpaidInvoicesAmount = outstandingInvoices.reduce(
                    (sum, invoice) => sum + Number(invoice.balance ?? 0),
                    0
                );

                setData({
                    kpis: {
                        ...normalizeKpis(kpisRes.status === 'fulfilled' ? kpisRes.value.data : {}),
                        unpaid_invoices_amount: unpaidInvoicesAmount,
                    },
                    monthlyRevenue: revenueRes.status === 'fulfilled' ? revenueRes.value.data : [],
                    outstandingInvoices,
                    recentSales: salesRes.status === 'fulfilled' ? salesRes.value.data : [],
                    lowStock: stockRes.status === 'fulfilled' ? stockRes.value.data : []
                });

                if ([kpisRes, revenueRes, salesRes, stockRes, outstandingRes].some(r => r.status === 'rejected')) {
                    console.warn('Some dashboard endpoints failed; rendered available data only.');
                }
            } catch (error) {
                console.warn('Dashboard API calls failed, rendering empty state values.');

                setData({
                    kpis: {
                        total_revenue: 0,
                        total_purchases_value: 0,
                        inventory_value: 0,
                        total_products: 0,
                        unpaid_invoices_amount: 0,
                        unpaid_invoices_count: 0,
                        low_stock_count: 0,
                        total_invoices: 0,
                    },
                    monthlyRevenue: [],
                    outstandingInvoices: [],
                    recentSales: [],
                    lowStock: []
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

    const { kpis, monthlyRevenue, outstandingInvoices, recentSales, lowStock } = data;

    const latestRevenue = monthlyRevenue[monthlyRevenue.length - 1]?.revenue ?? 0;
    const totalOutstandingAmount = outstandingInvoices.reduce(
        (sum, invoice) => sum + Number(invoice.balance ?? 0),
        0
    );

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
                    <p className="text-textMuted text-sm mt-1">Live business snapshot from your current ERP data.</p>
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
                            Latest month: {formatPKR(latestRevenue)}
                        </span>
                    </div>
                </div>

                <div onClick={() => navigate('/purchases')} className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative overflow-hidden cursor-pointer hover:border-primary/30 transition-colors">
                    <p className="text-textMuted text-sm font-medium">Total Purchases</p>
                    <div className="flex flex-col items-start justify-between mt-3 gap-2">
                        <h3 className="text-2xl font-extrabold text-slate-900">{formatPKR(kpis.total_purchases_value)}</h3>
                        <span className="text-amber-600 text-xs font-bold flex items-center justify-center bg-amber-50 px-2 py-1 rounded-full w-max">
                            {kpis.total_invoices} Total Invoices
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
                        <h3 className="text-2xl font-extrabold text-slate-900">{formatPKR(totalOutstandingAmount)}</h3>
                        <span className="text-rose-600 text-xs font-bold flex items-center justify-center bg-rose-50 px-2 py-1 rounded-full w-max">
                            <span className="material-symbols-outlined !text-xs mr-0.5">error</span>{kpis.unpaid_invoices_count} Overdue
                        </span>
                    </div>
                </div>
            </div>

            {/* Middle Section: Chart */}
            <div className="grid grid-cols-1 gap-6">

                {/* Recharts Area Flow (Dynamic replacement for HTML SVG) */}
                <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex flex-col">
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
                            <span className="bg-slate-50 rounded-lg text-xs font-bold py-1.5 px-3">
                                {monthlyRevenue.length} Data Points
                            </span>
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
                                <span className="text-emerald-600 text-right">{formatPKR(latestRevenue)}</span>
                            </div>
                            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                <div className="bg-emerald-500 h-full" style={{ width: `${Math.min(100, latestRevenue > 0 ? 70 : 0)}%` }}></div>
                            </div>
                        </div>

                        <div className="flex flex-col gap-1 mt-4 w-full">
                            <div className="flex justify-between items-center text-xs font-bold w-full">
                                <span className="text-textMuted text-left">Outflow (Current Month)</span>
                                <span className="text-rose-600 text-right">{formatPKR(kpis.total_purchases_value)}</span>
                            </div>
                            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                <div className="bg-rose-500 h-full" style={{ width: `${Math.min(100, kpis.total_purchases_value > 0 ? 55 : 0)}%` }}></div>
                            </div>
                        </div>

                        <div className="mt-6 p-4 rounded-lg bg-slate-50 border border-slate-200">
                            <p className="text-xs text-textMuted font-medium">Net Position</p>
                            <p className="text-xl font-extrabold text-primary pt-1">{formatPKR(latestRevenue - Number(kpis.total_purchases_value || 0))}</p>
                            <p className="text-[10px] text-emerald-600 font-bold mt-1">Computed from monthly revenue and total purchases</p>
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
                        {lowStock.length === 0 && (
                            <div className="p-4 border border-dashed border-gray-200 rounded-lg text-center text-sm text-textMuted">
                                No inventory items available yet.
                            </div>
                        )}
                        {lowStock.map((item, idx) => (
                            <div key={idx} className="flex items-center justify-between p-3 border border-gray-100 rounded-lg">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 bg-primary/10 rounded flex flex-shrink-0 items-center justify-center text-primary">
                                        {item.isReorder ? <AlertTriangle className="w-5 h-5" /> : <Package className="w-5 h-5" />}
                                    </div>
                                    <div className="min-w-0">
                                        <p className="text-sm font-bold truncate">{item.product_name}</p>
                                        <p className="text-[10px] text-textMuted">{item.stock_quantity} Units • {item.sku}</p>
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
                                        <p className="text-sm font-semibold truncate">Sale #{sale.sale_id} - {sale.customer_name}</p>
                                        <p className="text-[10px] text-textMuted">{sale.sale_date}</p>
                                    </div>
                                </div>
                                <p className="text-sm font-bold flex-shrink-0 ml-2 whitespace-nowrap text-textMain">
                                    {formatPKR(sale.total_price)}
                                </p>
                            </div>
                        ))}
                        {recentSales.length === 0 && (
                            <div className="text-sm text-textMuted">No recent sales found.</div>
                        )}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Dashboard;
