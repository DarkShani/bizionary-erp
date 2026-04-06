import React, { useState, useEffect } from 'react';
import { Mail, Phone, Calendar, AlertCircle, AlertTriangle } from 'lucide-react';
import { formatPKR } from '../../../utils/currency';
import { customerAnalyticsApi } from '../../../services/customerAnalyticsApi';

const CustomersTab = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                setLoading(true);
                const res = await customerAnalyticsApi.getCustomers();
                // Usually DRF ViewSet responses are an array or paginated object `{count, results: []}`
                if (res.data?.results) {
                    setCustomers(res.data.results);
                } else if (Array.isArray(res.data)) {
                    setCustomers(res.data);
                } else if (res.data?.data) {
                    setCustomers(res.data.data);
                }
            } catch (error) {
                console.warn('Failed to fetch customers.');
                setCustomers([]);
            } finally {
                setLoading(false);
            }
        };

        fetchCustomers();
    }, []);

    const getTierBadge = (tier) => {
        switch (tier) {
            case 'VIP': return 'bg-amber-100 text-amber-700 border-amber-200';
            case 'REGULAR': return 'bg-sky-100 text-sky-700 border-sky-200';
            case 'NEW': return 'bg-emerald-100 text-emerald-700 border-emerald-200';
            default: return 'bg-gray-100 text-gray-700 border-gray-200';
        }
    };

    if (loading) return <div className="text-center py-10"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div></div>;

    return (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
            <table className="w-full text-left border-collapse">
                <thead>
                    <tr className="bg-slate-50 border-b border-gray-100">
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider">Customer Name</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider">Contact Info</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider text-center">Tier</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider text-center">Last Purchase</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider text-right">Lifetime Value</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider text-center">Status</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                    {customers.length === 0 ? (
                        <tr>
                            <td colSpan="6" className="px-6 py-8 text-center text-textMuted text-sm">No customers found.</td>
                        </tr>
                    ) : (
                        (customers || []).map((customer) => (
                            <tr key={customer?.id || Math.random()} className="hover:bg-slate-50/50 transition-colors">
                                <td className="px-6 py-4">
                                    <p className="text-sm font-bold text-textMain">{customer.full_name}</p>
                                    <p className="text-[10px] text-textMuted font-medium uppercase mt-0.5">ID: {customer.id}</p>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-1.5 text-xs text-gray-600 mb-1">
                                        <Mail className="w-3.5 h-3.5 text-gray-400" />
                                        {customer.email || 'N/A'}
                                    </div>
                                    <div className="flex items-center gap-1.5 text-xs text-gray-600">
                                        <Phone className="w-3.5 h-3.5 text-gray-400" />
                                        {customer.phone || 'N/A'}
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <span className={`text-[10px] font-bold px-2 py-1 rounded-md border inline-block ${getTierBadge(customer.loyalty_tier)}`}>
                                        {customer.loyalty_tier}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <div className="flex items-center justify-center gap-1.5 text-sm text-gray-700">
                                        <Calendar className="w-4 h-4 text-gray-400" />
                                        {customer.last_purchase_date || 'Never'}
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <span className="text-sm font-bold text-slate-900">
                                        {formatPKR(customer.lifetime_value)}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    {customer.is_at_risk ? (
                                        <span className="inline-flex items-center gap-1 text-[10px] font-bold text-rose-600 bg-rose-50 px-2 pl-1.5 py-1 rounded-full border border-rose-100">
                                            <AlertTriangle className="w-3.5 h-3.5" />
                                            AT RISK
                                        </span>
                                    ) : (
                                        <span className="inline-flex items-center px-2 py-1 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-600 border border-emerald-100">
                                            ACTIVE
                                        </span>
                                    )}
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default CustomersTab;
