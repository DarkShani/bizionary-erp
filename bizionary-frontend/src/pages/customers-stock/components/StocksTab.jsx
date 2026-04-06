import React, { useState, useEffect } from 'react';
import { Package } from 'lucide-react';
import { formatPKR } from '../../../utils/currency';
import api from '../../../services/api';

const StocksTab = () => {
    const [stocks, setStocks] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStocks = async () => {
            try {
                setLoading(true);
                const res = await api.get('products/');
                const products = res.data?.data || res.data || [];

                setStocks(products.map((item) => ({
                    id: item.id,
                    sku: item.sku,
                    name: item.name,
                    category: item.category,
                    quantity: item.stock_quantity,
                    low_stock_threshold: item.reorder_level,
                    unit_price: item.unit_price,
                    value: Number(item.stock_quantity || 0) * Number(item.unit_price || 0),
                })));
            } catch (error) {
                console.warn('Failed to fetch stock data from products API.');
                setStocks([]);
            } finally {
                setLoading(false);
            }
        };

        fetchStocks();
    }, []);

    if (loading) return <div className="text-center py-10"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div></div>;

    return (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
            <table className="w-full text-left border-collapse">
                <thead>
                    <tr className="bg-slate-50 border-b border-gray-100">
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider">Product Name & SKU</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider">Category</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider text-center">In Stock</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider text-right">Unit Price</th>
                        <th className="px-6 py-4 text-xs font-bold text-textMuted uppercase tracking-wider text-right">Total Value</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                    {stocks.length === 0 && (
                        <tr>
                            <td colSpan="5" className="px-6 py-8 text-center text-textMuted text-sm">No stock records found.</td>
                        </tr>
                    )}
                    {stocks.map((item) => (
                        <tr key={item.id} className="hover:bg-slate-50/50 transition-colors">
                            <td className="px-6 py-4">
                                <div className="flex items-center gap-2">
                                    <div className="w-8 h-8 rounded bg-slate-100 flex flex-shrink-0 items-center justify-center text-slate-400">
                                        <Package className="w-4 h-4" />
                                    </div>
                                    <div className="min-w-0">
                                        <p className="text-sm font-bold text-textMain truncate">{item.name}</p>
                                        <p className="text-[10px] text-textMuted font-bold uppercase mt-0.5">{item.sku}</p>
                                    </div>
                                </div>
                            </td>
                            <td className="px-6 py-4 text-sm font-semibold text-gray-700">
                                {item.category}
                            </td>
                            <td className="px-6 py-4 text-center">
                                <span className={`text-sm font-bold px-3 py-1 rounded-full ${item.quantity <= item.low_stock_threshold ? 'bg-rose-100 text-rose-700' : 'bg-slate-100 text-slate-700'}`}>
                                    {item.quantity} Units
                                </span>
                                {item.quantity <= item.low_stock_threshold && (
                                    <p className="text-[10px] text-rose-500 font-bold mt-1">Reorder <br/> (Below {item.low_stock_threshold})</p>
                                )}
                            </td>
                            <td className="px-6 py-4 text-right">
                                <span className="text-sm text-gray-600 font-medium">
                                    {formatPKR(item.unit_price)}
                                </span>
                            </td>
                            <td className="px-6 py-4 text-right">
                                <span className="text-sm font-bold text-emerald-700">
                                    {formatPKR(item.value)}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default StocksTab;
