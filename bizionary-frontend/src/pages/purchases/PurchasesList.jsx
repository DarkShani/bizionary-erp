import React, { useState, useEffect } from 'react';
import { Plus, Search, Edit2, Trash2, Filter, ShoppingBag } from 'lucide-react';
import { formatPKR } from '../../utils/currency';
import api from '../../services/api';
import PurchaseForm from './PurchaseForm';

const PurchasesList = () => {
    const [purchases, setPurchases] = useState([]);
    const [loading, setLoading] = useState(true);

    // UI States
    const [searchTerm, setSearchTerm] = useState('');
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [currentPurchase, setCurrentPurchase] = useState(null);

    useEffect(() => {
        fetchPurchases();
    }, []);

    const fetchPurchases = async () => {
        try {
            setLoading(true);
            const res = await api.get('purchases/');
            let data = res.data.data || res.data;
            setPurchases(data);
        } catch (error) {
            console.warn('Failed to fetch purchases from backend.');
            setPurchases([]);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateOrUpdate = async (purchaseData) => {
        try {
            if (currentPurchase) {
                await api.put(`purchases/${currentPurchase.id}/`, purchaseData);
            } else {
                await api.post('purchases/', purchaseData);
            }
            await fetchPurchases();
            setIsFormOpen(false);
            setCurrentPurchase(null);
        } catch (error) {
            alert("Failed to save purchase.");
        }
    };

    const handleDelete = async (id) => {
        try {
            await api.delete(`purchases/${id}/`);
            await fetchPurchases();
        } catch (error) {
            alert("Failed to delete purchase.");
        }
    };

    const openAddForm = () => {
        setCurrentPurchase(null);
        setIsFormOpen(true);
    };

    const openEditForm = (item) => {
        setCurrentPurchase(item);
        setIsFormOpen(true);
    };

    const filteredPurchases = purchases.filter(p =>
        (p.product_name && p.product_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (p.supplier_name && p.supplier_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        p.id.toString().includes(searchTerm)
    );

    return (
        <div className="space-y-6">

            {/* Header Actions */}
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div className="relative flex-1 max-w-md">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Search className="h-4 w-4 text-gray-400" />
                    </div>
                    <input
                        type="text"
                        className="block w-full pl-10 pr-3 py-2 border border-gray-100 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-sm bg-surface shadow-sm text-textMain placeholder-textMuted"
                        placeholder="Search by product, vendor, or ID..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                <div className="flex items-center gap-3 w-full sm:w-auto">
                    <button className="flex items-center justify-center px-4 py-2 border border-gray-100 text-textMuted bg-surface rounded-xl hover:bg-slate-50 text-sm font-semibold transition-colors shadow-sm w-full sm:w-auto">
                        <Filter className="h-4 w-4 mr-2" />
                        Filters
                    </button>
                    <button
                        onClick={openAddForm}
                        className="flex items-center justify-center px-4 py-2 bg-primary text-white rounded-xl hover:bg-primaryDark text-sm font-bold transition-all shadow-md shadow-primary/20 w-full sm:w-auto"
                    >
                        <Plus className="h-4 w-4 mr-2" />
                        New Purchase
                    </button>
                </div>
            </div>

            {/* Main Table */}
            <div className="bg-surface rounded-3xl border border-gray-100 shadow-sm overflow-hidden flex flex-col">
                {loading ? (
                    <div className="h-64 flex items-center justify-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-white text-textMuted text-xs uppercase tracking-wider border-b border-gray-100">
                                <tr>
                                    <th className="px-6 py-4 font-semibold">PO #</th>
                                    <th className="px-6 py-4 font-semibold">Date</th>
                                    <th className="px-6 py-4 font-semibold">Vendor</th>
                                    <th className="px-6 py-4 font-semibold">Product</th>
                                    <th className="px-6 py-4 font-semibold text-center">Qty</th>
                                    <th className="px-6 py-4 font-semibold text-right">Total Cost</th>
                                    <th className="px-6 py-4 font-semibold text-center">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-50">
                                {filteredPurchases.map((p) => (
                                    <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap text-textMuted font-mono text-xs">PO-{p.id.toString().padStart(4, '0')}</td>
                                        <td className="px-6 py-4 text-textMuted">{p.purchase_date}</td>
                                        <td className="px-6 py-4 font-medium text-textMain">{p.supplier_name}</td>
                                        <td className="px-6 py-4 font-bold text-textMain">{p.product_name || `Product ID: ${p.product}`}</td>
                                        <td className="px-6 py-4 text-center">
                                            <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-50 text-purple-700 border border-purple-100">
                                                {p.quantity_purchased}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 font-bold text-danger text-right">{formatPKR(p.total_cost)}</td>
                                        <td className="px-6 py-4 text-center">
                                            <div className="flex items-center justify-center gap-3">
                                                <button
                                                    onClick={() => openEditForm(p)}
                                                    className="text-gray-400 hover:text-primary transition-colors"
                                                    title="Edit"
                                                >
                                                    <Edit2 className="h-4 w-4" />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(p.id)}
                                                    className="text-gray-400 hover:text-danger hover:fill-danger/10 transition-colors"
                                                    title="Delete"
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                                {filteredPurchases.length === 0 && (
                                    <tr>
                                        <td colSpan="7" className="px-6 py-12 text-center text-textMuted">
                                            <ShoppingBag className="mx-auto h-12 w-12 text-gray-300 mb-3" />
                                            <p>No purchase records found.</p>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <PurchaseForm
                isOpen={isFormOpen}
                onClose={() => setIsFormOpen(false)}
                onSubmit={handleCreateOrUpdate}
                initialData={currentPurchase}
            />
        </div>
    );
};

export default PurchasesList;
