import React, { useState, useEffect } from 'react';
import { Dialog } from '@headlessui/react';
import { X } from 'lucide-react';
import api from '../../services/api';

const SaleForm = ({ isOpen, onClose, onSubmit, initialData }) => {
    const isEditing = !!initialData;
    const [products, setProducts] = useState([]);

    const [formData, setFormData] = useState({
        product: '',
        product_name: '', // Added so the mock frontend can display the name easily
        customer_name: '',
        quantity_sold: 1,
        unit_price: 0,
    });

    useEffect(() => {
        // Fetch products for the dropdown
        const fetchProducts = async () => {
            try {
                const res = await api.get('products/');
                setProducts(res.data.data || res.data);
            } catch (error) {
                // Fallback Mock Data
                setProducts([
                    { id: 1, name: 'A4 Copy Paper 80 GSM', unit_price: 1500 },
                    { id: 2, name: 'Office Chair Exec', unit_price: 18000 },
                    { id: 3, name: 'Wireless Mouse', unit_price: 2500 },
                    { id: 4, name: 'Stapler Pro', unit_price: 450 },
                    { id: 5, name: 'Printer Ink Black', unit_price: 3500 },
                ]);
            }
        };
        fetchProducts();
    }, []);

    useEffect(() => {
        if (initialData) {
            setFormData(initialData);
        } else {
            setFormData({
                product: '',
                product_name: '',
                customer_name: '',
                quantity_sold: 1,
                unit_price: 0,
            });
        }
    }, [initialData, isOpen]);

    const handleChange = (e) => {
        const { name, value, type } = e.target;

        let newFormData = {
            ...formData,
            [name]: type === 'number' ? Number(value) : value,
        };

        // If product is selected, auto-fill unit_price and product_name for convenience
        if (name === 'product') {
            const selectedProduct = products.find(p => p.id === Number(value));
            if (selectedProduct) {
                newFormData.unit_price = selectedProduct.unit_price;
                newFormData.product_name = selectedProduct.name;
            }
        }

        setFormData(newFormData);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <Dialog open={isOpen} onClose={onClose} className="relative z-50">
            <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

            <div className="fixed inset-0 flex items-center justify-center p-4">
                <Dialog.Panel className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl border border-gray-100">
                    <div className="flex justify-between items-center mb-6">
                        <Dialog.Title className="text-xl font-bold text-textMain">
                            {isEditing ? 'Edit Sale' : 'Create New Sale'}
                        </Dialog.Title>
                        <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-50">
                            <X className="w-5 h-5" />
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">

                            <div className="col-span-2">
                                <label className="block text-sm font-medium text-gray-700 mb-1">Customer Name</label>
                                <input
                                    type="text"
                                    name="customer_name"
                                    required
                                    value={formData.customer_name}
                                    onChange={handleChange}
                                    className="w-full border border-gray-200 rounded-lg p-2.5 outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
                                    placeholder="e.g. John Doe"
                                />
                            </div>

                            <div className="col-span-2">
                                <label className="block text-sm font-medium text-gray-700 mb-1">Product</label>
                                <select
                                    name="product"
                                    required
                                    value={formData.product}
                                    onChange={handleChange}
                                    className="w-full border border-gray-200 rounded-lg p-2.5 outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-sm bg-white"
                                >
                                    <option value="" disabled>Select a product...</option>
                                    {products.map(p => (
                                        <option key={p.id} value={p.id}>{p.name}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="col-span-2 sm:col-span-1">
                                <label className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                                <input
                                    type="number"
                                    name="quantity_sold"
                                    min="1"
                                    required
                                    value={formData.quantity_sold}
                                    onChange={handleChange}
                                    className="w-full border border-gray-200 rounded-lg p-2.5 outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
                                />
                            </div>

                            <div className="col-span-2 sm:col-span-1">
                                <label className="block text-sm font-medium text-gray-700 mb-1">Unit Price (Rs)</label>
                                <input
                                    type="number"
                                    name="unit_price"
                                    min="0"
                                    step="0.01"
                                    required
                                    value={formData.unit_price}
                                    onChange={handleChange}
                                    className="w-full border border-gray-200 rounded-lg p-2.5 outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-sm bg-gray-50"
                                />
                            </div>

                        </div>

                        {/* Calculated Total */}
                        <div className="mt-4 p-4 bg-sky-50 rounded-xl border border-sky-100 flex justify-between items-center">
                            <span className="text-sm font-semibold text-sky-800">Total Price:</span>
                            <span className="text-xl font-bold text-primary">
                                Rs {(formData.quantity_sold * formData.unit_price).toLocaleString()}
                            </span>
                        </div>

                        <div className="mt-8 flex justify-end gap-3 pt-4 border-t border-gray-50">
                            <button
                                type="button"
                                onClick={onClose}
                                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition-colors"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                className="px-4 py-2 text-sm font-medium text-white bg-primary rounded-xl hover:bg-primaryDark transition-colors"
                            >
                                {isEditing ? 'Save Changes' : 'Create Sale'}
                            </button>
                        </div>
                    </form>
                </Dialog.Panel>
            </div>
        </Dialog>
    );
};

export default SaleForm;
