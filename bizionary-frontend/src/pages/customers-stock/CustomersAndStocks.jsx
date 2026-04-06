import React, { useState, useEffect } from 'react';
import { Users, Package, BarChart3, TrendingUp, UserCheck, AlertTriangle } from 'lucide-react';
import { formatPKR } from '../../utils/currency';
import { customerAnalyticsApi } from '../../services/customerAnalyticsApi';
import CustomersTab from './components/CustomersTab';
import StocksTab from './components/StocksTab';
import AnalyticsTab from './components/AnalyticsTab';

const CustomersAndStocks = () => {
    const [activeTab, setActiveTab] = useState('customers');
    const [kpis, setKpis] = useState(null);
    const [loadingKpis, setLoadingKpis] = useState(true);

    useEffect(() => {
        const fetchKpis = async () => {
            try {
                setLoadingKpis(true);
                const res = await customerAnalyticsApi.getDashboardKpis();
                if (res.data) {
                    setKpis(res.data);
                }
            } catch (error) {
                console.warn('Failed to fetch customer analytics KPIs.');
                setKpis({
                    total_customers: 0,
                    total_customers_change: 0,
                    retention_rate: 0,
                    retention_rate_change: 0,
                    avg_lifetime_value: 0,
                    avg_lifetime_value_change: 0,
                    churn_risk_percentage: 0,
                    churn_risk_change: 0
                });
            } finally {
                setLoadingKpis(false);
            }
        };

        fetchKpis();
    }, []);

    const renderChange = (value) => {
        const isPositive = value >= 0;
        const colorClass = isPositive ? 'text-emerald-600 bg-emerald-50' : 'text-rose-600 bg-rose-50';
        const icon = isPositive ? 'trending_up' : 'trending_down';
        return (
            <span className={`text-xs font-bold flex items-center justify-center px-2 py-1 rounded-full w-max ${colorClass}`}>
                <span className="material-symbols-outlined !text-xs mr-0.5">{icon}</span>
                {Math.abs(value)}%
            </span>
        );
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold text-textMain">Customers & Stocks</h1>
                    <p className="text-sm text-textMuted mt-1">Manage customer analytics and inventory availability.</p>
                </div>
            </div>

            {/* KPI Summary Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4">
                    <div className="p-3 bg-sky-50 text-sky-600 rounded-lg">
                        <Users className="w-6 h-6" />
                    </div>
                    <div className="flex flex-col flex-1 items-start justify-between gap-2">
                        <p className="text-xs text-textMuted font-medium w-full">Total Customers</p>
                        <h4 className="text-lg font-bold text-slate-900">
                            {loadingKpis ? '...' : kpis?.total_customers?.toLocaleString()}
                        </h4>
                        {!loadingKpis && kpis?.total_customers_change !== undefined && renderChange(kpis.total_customers_change)}
                    </div>
                </div>
                
                <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4">
                    <div className="p-3 bg-emerald-50 text-emerald-600 rounded-lg">
                        <UserCheck className="w-6 h-6" />
                    </div>
                    <div className="flex flex-col flex-1 items-start justify-between gap-2">
                        <p className="text-xs text-textMuted font-medium w-full">Retention Rate</p>
                        <h4 className="text-lg font-bold text-slate-900">
                            {loadingKpis ? '...' : `${kpis?.retention_rate}%`}
                        </h4>
                        {!loadingKpis && kpis?.retention_rate_change !== undefined && renderChange(kpis.retention_rate_change)}
                    </div>
                </div>

                <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4">
                    <div className="p-3 bg-primary/10 text-primary rounded-lg">
                        <TrendingUp className="w-6 h-6" />
                    </div>
                    <div className="flex flex-col flex-1 items-start justify-between gap-2">
                        <p className="text-xs text-textMuted font-medium w-full">Avg Lifetime Value</p>
                        <h4 className="text-lg font-bold text-slate-900">
                            {loadingKpis ? '...' : formatPKR(kpis?.avg_lifetime_value || 0)}
                        </h4>
                        {!loadingKpis && kpis?.avg_lifetime_value_change !== undefined && renderChange(kpis.avg_lifetime_value_change)}
                    </div>
                </div>

                <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4">
                    <div className="p-3 bg-amber-50 text-amber-600 rounded-lg">
                        <AlertTriangle className="w-6 h-6" />
                    </div>
                    <div className="flex flex-col flex-1 items-start justify-between gap-2">
                        <p className="text-xs text-textMuted font-medium w-full">Churn Risk</p>
                        <h4 className="text-lg font-bold text-slate-900">
                            {loadingKpis ? '...' : `${kpis?.churn_risk_percentage}%`}
                        </h4>
                        {!loadingKpis && kpis?.churn_risk_change !== undefined && renderChange(kpis.churn_risk_change)}
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden flex flex-col h-full min-h-[500px]">
                <div className="flex border-b border-gray-100 px-6 pt-4 gap-6">
                    <button
                        onClick={() => setActiveTab('customers')}
                        className={`flex items-center gap-2 pb-4 font-semibold text-sm transition-colors relative ${activeTab === 'customers' ? 'text-primary' : 'text-gray-500 hover:text-gray-900'}`}
                    >
                        <Users className="w-4 h-4" />
                        Customers List
                        {activeTab === 'customers' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-primary rounded-t-full"></div>}
                    </button>
                    <button
                        onClick={() => setActiveTab('stocks')}
                        className={`flex items-center gap-2 pb-4 font-semibold text-sm transition-colors relative ${activeTab === 'stocks' ? 'text-primary' : 'text-gray-500 hover:text-gray-900'}`}
                    >
                        <Package className="w-4 h-4" />
                        Inventory Stocks
                        {activeTab === 'stocks' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-primary rounded-t-full"></div>}
                    </button>
                    <button
                        onClick={() => setActiveTab('analytics')}
                        className={`flex items-center gap-2 pb-4 font-semibold text-sm transition-colors relative ${activeTab === 'analytics' ? 'text-primary' : 'text-gray-500 hover:text-gray-900'}`}
                    >
                        <BarChart3 className="w-4 h-4" />
                        Behavior Analytics
                        {activeTab === 'analytics' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-primary rounded-t-full"></div>}
                    </button>
                </div>

                <div className="p-6 flex-1 bg-slate-50/50">
                    {activeTab === 'customers' && <CustomersTab />}
                    {activeTab === 'stocks' && <StocksTab />}
                    {activeTab === 'analytics' && <AnalyticsTab />}
                </div>
            </div>
        </div>
    );
};

export default CustomersAndStocks;
