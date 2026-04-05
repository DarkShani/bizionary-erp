import React, { useState, useEffect } from 'react';
import { Plus, Search, Edit2, Trash2, Filter, Receipt } from 'lucide-react';
import { formatPKR } from '../../utils/currency';
import api from '../../services/api';
import SaleForm from './SaleForm';

const SalesList = () => {
    const [sales, setSales] = useState([]);
    const [loading, setLoading] = useState(true);

    // UI States
    const [searchTerm, setSearchTerm] = useState('');
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [currentSale, setCurrentSale] = useState(null);

    useEffect(() => {
        fetchSales();
    }, []);

    const fetchSales = async () => {
        try {
            setLoading(true);
            const res = await api.get('sales/');
            let data = res.data.data || res.data;
            // Ensure date sorting or transformations if needed
            setSales(data);
        } catch (error) {
            console.warn("Failed to fetch sales from backend, using mock data for demo.");
            // Fallback Mock Data
            setSales([
                { id: 1, product: 1, product_name: 'A4 Copy Paper 80 GSM', customer_name: 'Tech Solutions Inc', quantity_sold: 50, unit_price: 1500, total_price: 75000, sale_date: '2024-05-15' },
                { id: 2, product: 2, product_name: 'Office Chair Exec', customer_name: 'Startup Hub', quantity_sold: 4, unit_price: 18000, total_price: 72000, sale_date: '2024-05-16' },
                { id: 3, product: 3, product_name: 'Wireless Mouse', customer_name: 'Freelancer Co', quantity_sold: 10, unit_price: 2500, total_price: 25000, sale_date: '2024-05-16' },
                { id: 4, product: 4, product_name: 'Stapler Pro', customer_name: 'Local School', quantity_sold: 25, unit_price: 450, total_price: 11250, sale_date: '2024-05-17' },
                { id: 5, product: 5, product_name: 'Printer Ink Black', customer_name: 'Tech Solutions Inc', quantity_sold: 2, unit_price: 3500, total_price: 7000, sale_date: '2024-05-18' },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateOrUpdate = async (saleData) => {
        try {
            if (currentSale) {
                // Update
                // await api.put(`sales/${currentSale.id}/`, saleData);
                // The mock logic below manually calculates total_price if the backend isn't there
                const updatedObj = { ...currentSale, ...saleData, total_price: saleData.quantity_sold * saleData.unit_price };
                setSales(prev => prev.map(s => s.id === currentSale.id ? updatedObj : s));
            } else {
                // Create
                // const res = await api.post('sales/', saleData);
                // setSales([...sales, res.data]);

                // Mock Add
                const newObj = { ...saleData, id: Date.now(), total_price: saleData.quantity_sold * saleData.unit_price, sale_date: new Date().toISOString().split('T')[0] };
                setSales(prev => [newObj, ...prev]);
            }
            setIsFormOpen(false);
            setCurrentSale(null);
        } catch (error) {
            alert("Failed to save sale.");
        }
    };

    const handleDelete = async (id) => {
        try {
            // await api.delete(`sales/${id}/`);
            setSales(prev => prev.filter(s => s.id !== id));
        } catch (error) {
            alert("Failed to delete sale.");
        }
    };

    const openAddForm = () => {
        setCurrentSale(null);
        setIsFormOpen(true);
    };

    const openEditForm = (item) => {
        setCurrentSale(item);
        setIsFormOpen(true);
    };

    const filteredSales = sales.filter(s =>
        (s.product_name && s.product_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (s.customer_name && s.customer_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        s.id.toString().includes(searchTerm)
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
                        placeholder="Search by product, customer, or ID..."
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
                        New Sale
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
                                    <th className="px-6 py-4 font-semibold">Ref ID</th>
                                    <th className="px-6 py-4 font-semibold">Date</th>
                                    <th className="px-6 py-4 font-semibold">Customer</th>
                                    <th className="px-6 py-4 font-semibold">Product</th>
                                    <th className="px-6 py-4 font-semibold text-center">Qty</th>
                                    <th className="px-6 py-4 font-semibold text-right">Total Price</th>
                                    <th className="px-6 py-4 font-semibold text-center">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-50">
                                {filteredSales.map((s) => (
                                    <tr key={s.id} className="hover:bg-slate-50 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap text-textMuted font-mono text-xs">#SL-{s.id.toString().padStart(4, '0')}</td>
                                        <td className="px-6 py-4 text-textMuted">{s.sale_date}</td>
                                        <td className="px-6 py-4 font-medium text-textMain">{s.customer_name}</td>
                                        <td className="px-6 py-4 font-bold text-textMain">{s.product_name || `Product ID: ${s.product}`}</td>
                                        <td className="px-6 py-4 text-center">
                                            <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-bold bg-sky-50 text-sky-700 border border-sky-100">
                                                {s.quantity_sold}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 font-bold text-success text-right">{formatPKR(s.total_price)}</td>
                                        <td className="px-6 py-4 text-center">
                                            <div className="flex items-center justify-center gap-3">
                                                <button
                                                    onClick={() => openEditForm(s)}
                                                    className="text-gray-400 hover:text-primary transition-colors"
                                                    title="Edit"
                                                >
                                                    <Edit2 className="h-4 w-4" />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(s.id)}
                                                    className="text-gray-400 hover:text-danger hover:fill-danger/10 transition-colors"
                                                    title="Delete"
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                                {filteredSales.length === 0 && (
                                    <tr>
                                        <td colSpan="7" className="px-6 py-12 text-center text-textMuted">
                                            <Receipt className="mx-auto h-12 w-12 text-gray-300 mb-3" />
                                            <p>No sales records found.</p>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <SaleForm
                isOpen={isFormOpen}
                onClose={() => setIsFormOpen(false)}
                onSubmit={handleCreateOrUpdate}
                initialData={currentSale}
            />
        </div>
    );
};

export default SalesList;
