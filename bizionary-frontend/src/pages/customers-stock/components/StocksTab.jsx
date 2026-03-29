import React, { useState, useEffect } from 'react';
import { Package, AlertCircle } from 'lucide-react';
import { formatPKR } from '../../../utils/currency';

const StocksTab = () => {
    const [stocks, setStocks] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Mock dataset since explicit backend for stocks wasn't provided yet
        setTimeout(() => {
            setStocks([
                { id: 101, sku: 'TECH-LAP-01', name: 'MacBook Pro 14"', category: 'Electronics', quantity: 24, low_stock_threshold: 10, unit_price: 450000, value: 10800000 },
                { id: 102, sku: 'OFF-CHR-05', name: 'Ergonomic Office Chair', category: 'Furniture', quantity: 8, low_stock_threshold: 15, unit_price: 35000, value: 280000 },
                { id: 103, sku: 'STAT-PAP-A4', name: 'A4 Printer Paper (Box)', category: 'Stationery', quantity: 145, low_stock_threshold: 50, unit_price: 4500, value: 652500 },
                { id: 104, sku: 'TECH-MOU-02', name: 'Wireless Mouse', category: 'Accessories', quantity: 4, low_stock_threshold: 20, unit_price: 2500, value: 10000 }
            ]);
            setLoading(false);
        }, 800);
    }, []);

    if (loading) return <div className="text-center py-10"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div></div>;

    return (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
            <div className="p-4 bg-amber-50 border-b border-amber-100 flex items-center gap-3 text-amber-800">
                <AlertCircle className="w-5 h-5" />
                <p className="text-sm font-medium"><strong>Notice:</strong> This is a mock inventory table. Connect to the real products API when available.</p>
            </div>
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
