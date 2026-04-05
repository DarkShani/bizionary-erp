import React, { useState, useEffect } from 'react';
import { Plus, Search, Edit2, Trash2, Filter } from 'lucide-react';
import { formatPKR } from '../../utils/currency';
import api from '../../services/api';
import ProductForm from './ProductForm';

const ProductList = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    // UI States
    const [searchTerm, setSearchTerm] = useState('');
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [currentProduct, setCurrentProduct] = useState(null);

    useEffect(() => {
        fetchProducts();
    }, []);

    const fetchProducts = async () => {
        try {
            setLoading(true);
            const res = await api.get('products/');
            setProducts(res.data.data || res.data); // handles {data: []} or just []
        } catch (error) {
            console.warn("Failed to fetch products from backend, using mock data for demo.");
            // Fallback Mock Data
            setProducts([
                { id: 1, name: 'A4 Copy Paper 80 GSM', sku: 'PAP-A4-80', stock_quantity: 500, reorder_level: 100, unit_price: 1500, category: 'Office Supplies' },
                { id: 2, name: 'Office Chair Exec', sku: 'FURN-CHR-01', stock_quantity: 15, reorder_level: 5, unit_price: 18000, category: 'Furniture' },
                { id: 3, name: 'Wireless Mouse', sku: 'TECH-MOU-W', stock_quantity: 45, reorder_level: 20, unit_price: 2500, category: 'Electronics' },
                { id: 4, name: 'Stapler Pro', sku: 'OFF-STP-01', stock_quantity: 120, reorder_level: 50, unit_price: 450, category: 'Office Supplies' },
                { id: 5, name: 'Printer Ink Black', sku: 'INK-BLK-01', stock_quantity: 8, reorder_level: 20, unit_price: 3500, category: 'Electronics' },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateOrUpdate = async (productData) => {
        try {
            if (currentProduct) {
                // Update
                // await api.put(`products/${currentProduct.id}/`, productData);
                setProducts(prev => prev.map(p => p.id === currentProduct.id ? { ...p, ...productData } : p));
            } else {
                // Create
                // const res = await api.post('products/', productData);
                // setProducts([...products, res.data]);

                // Mock Add
                setProducts(prev => [{ ...productData, id: Date.now() }, ...prev]);
            }
            setIsFormOpen(false);
            setCurrentProduct(null);
        } catch (error) {
            alert("Failed to save product.");
        }
    };

    const handleDelete = async (id) => {
        try {
            // await api.delete(`products/${id}/`);
            setProducts(prev => prev.filter(p => p.id !== id));
        } catch (error) {
            alert("Failed to delete product.");
        }
    };

    const openAddForm = () => {
        setCurrentProduct(null);
        setIsFormOpen(true);
    };

    const openEditForm = (item) => {
        setCurrentProduct(item);
        setIsFormOpen(true);
    };

    const filteredProducts = products.filter(p =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.sku.toLowerCase().includes(searchTerm.toLowerCase())
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
                        placeholder="Search by product name or SKU..."
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
                        Add Product
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
                                    <th className="px-6 py-4 font-semibold">SKU</th>
                                    <th className="px-6 py-4 font-semibold">Product Name</th>
                                    <th className="px-6 py-4 font-semibold">Category</th>
                                    <th className="px-6 py-4 font-semibold text-right">Unit Price</th>
                                    <th className="px-6 py-4 font-semibold text-center">Stock</th>
                                    <th className="px-6 py-4 font-semibold text-center">Reorder Lvl</th>
                                    <th className="px-6 py-4 font-semibold text-center">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-50">
                                {filteredProducts.map((p) => {
                                    const isLowStock = p.stock_quantity <= p.reorder_level;
                                    return (
                                        <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                                            <td className="px-6 py-4 whitespace-nowrap text-textMuted font-mono text-xs">{p.sku}</td>
                                            <td className="px-6 py-4 font-bold text-textMain">{p.name}</td>
                                            <td className="px-6 py-4 text-textMuted">{p.category || 'N/A'}</td>
                                            <td className="px-6 py-4 font-bold text-textMain text-right">{formatPKR(p.unit_price)}</td>
                                            <td className="px-6 py-4 text-center">
                                                <span className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-bold ${isLowStock ? 'bg-red-50 text-danger border border-red-100' : 'bg-green-50 text-success border border-green-100'}`}>
                                                    {p.stock_quantity}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-center text-textMuted font-medium">{p.reorder_level}</td>
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
                                    )
                                })}
                                {filteredProducts.length === 0 && (
                                    <tr>
                                        <td colSpan="7" className="px-6 py-12 text-center text-textMuted">
                                            <Search className="mx-auto h-12 w-12 text-gray-300 mb-3" />
                                            <p>No products found matching your search.</p>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Slide-over or Modal for Form */}
            <ProductForm
                isOpen={isFormOpen}
                onClose={() => setIsFormOpen(false)}
                onSubmit={handleCreateOrUpdate}
                initialData={currentProduct}
            />
        </div>
    );
};

export default ProductList;
