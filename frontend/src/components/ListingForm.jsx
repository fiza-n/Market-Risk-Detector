import React, { useState, useEffect } from 'react';
import { ArrowRight, Layers3, Sparkles } from 'lucide-react';
import { fetchCategories } from '../api/client.js';

const EXAMPLE_LISTING = {
  title: 'iPhone 14 Pro Max 256GB — PTA Approved (Urgent Sale)',
  description: 'Brand new sealed pack. Shifting abroad urgently, only serious buyers. Advance payment required via JazzCash/EasyPaisa to reserve item before dispatch. COD not available due to courier issues. WhatsApp for instant delivery details.',
  price: '145000',
  category: 'Mobile Phones',
  seller_info: 'Ali R. · Lahore · Account created 2 days ago'
};

export function ListingForm({ onSubmit, loading }) {
  const [categories, setCategories] = useState([
    "Mobile Phones", "Electronics", "Vehicles", "Furniture", "Fashion", "Property/Rent", "Other"
  ]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    category: 'Mobile Phones',
    seller_info: ''
  });

  useEffect(() => {
    fetchCategories().then((cats) => {
      if (cats && cats.length > 0) {
        setCategories(cats);
        if (!formData.category) {
          setFormData((prev) => ({ ...prev, category: cats[0] }));
        }
      }
    });
  }, []);

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleLoadExample = () => {
    setFormData(EXAMPLE_LISTING);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.title || !formData.description) return;
    onSubmit(formData);
  };

  return (
    <div className="grid gap-10 lg:grid-cols-[1fr_320px]">
      <form onSubmit={handleSubmit} className="rounded-3xl border border-border bg-card p-6 md:p-8 shadow-sm">
        <div className="flex items-center justify-between mb-6 pb-4 border-b border-border/60">
          <div>
            <h2 className="text-xl font-bold text-foreground">Listing Information</h2>
            <p className="text-xs text-muted-foreground mt-0.5">Paste text from OLX, Facebook Marketplace, or Daraz</p>
          </div>
          <button
            type="button"
            onClick={handleLoadExample}
            className="inline-flex items-center gap-1.5 rounded-full border border-border bg-secondary/50 px-3 py-1.5 text-xs font-semibold text-primary hover:bg-secondary transition-colors"
          >
            <Sparkles size={14} className="text-accent" />
            Load Sample Scam Listing
          </button>
        </div>

        <div className="grid gap-6">
          <label className="grid gap-2 text-sm font-bold text-foreground">
            Listing Title *
            <input
              type="text"
              required
              placeholder="e.g. iPhone 14 Pro Max 256GB PTA Approved"
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              className="h-11 rounded-xl border border-input bg-background px-4 font-normal outline-none focus:ring-2 focus:ring-ring text-foreground"
            />
          </label>

          <label className="grid gap-2 text-sm font-bold text-foreground">
            Description / Listing Text *
            <textarea
              required
              rows={6}
              placeholder="Paste full seller description here (include details about payment, delivery, warranty, or seller demands)..."
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              className="rounded-xl border border-input bg-background px-4 py-3 font-normal outline-none focus:ring-2 focus:ring-ring text-foreground resize-y"
            />
          </label>

          <div className="grid gap-6 sm:grid-cols-2">
            <label className="grid gap-2 text-sm font-bold text-foreground">
              Asking Price (PKR) *
              <input
                type="number"
                required
                min="0"
                placeholder="e.g. 145000"
                value={formData.price}
                onChange={(e) => handleChange('price', e.target.value)}
                className="h-11 rounded-xl border border-input bg-background px-4 font-normal outline-none focus:ring-2 focus:ring-ring text-foreground"
              />
            </label>

            <label className="grid gap-2 text-sm font-bold text-foreground">
              Category *
              <select
                value={formData.category}
                onChange={(e) => handleChange('category', e.target.value)}
                className="h-11 rounded-xl border border-input bg-background px-3 font-normal outline-none focus:ring-2 focus:ring-ring text-foreground cursor-pointer"
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <label className="grid gap-2 text-sm font-bold text-foreground">
            Seller Info (Optional)
            <input
              type="text"
              placeholder="e.g. Ali R. · Lahore · Account created 2 days ago"
              value={formData.seller_info}
              onChange={(e) => handleChange('seller_info', e.target.value)}
              className="h-11 rounded-xl border border-input bg-background px-4 font-normal outline-none focus:ring-2 focus:ring-ring text-foreground"
            />
          </label>
        </div>

        <button
          type="submit"
          disabled={loading || !formData.title || !formData.description}
          className="mt-8 w-full rounded-xl bg-primary px-5 py-3.5 font-bold text-primary-foreground disabled:opacity-60 transition-all flex items-center justify-center gap-2 hover:bg-primary/90 shadow-md shadow-primary/10"
        >
          {loading ? (
            <>
              <span className="inline-block size-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></span>
              Running AI Risk Analysis...
            </>
          ) : (
            <>
              Analyze This Listing <ArrowRight size={18} />
            </>
          )}
        </button>
      </form>

      <aside className="h-fit rounded-3xl bg-secondary p-6 border border-border/50">
        <div className="flex items-center gap-3">
          <Layers3 className="text-primary" size={22} />
          <strong className="text-base text-foreground font-bold">What Happens Next</strong>
        </div>
        <div className="mt-6 flex flex-col gap-5 text-sm text-foreground/90 leading-relaxed">
          <p className="flex gap-3">
            <b className="text-primary font-mono text-base">A</b>
            <span>Your listing details are parsed securely in real-time.</span>
          </p>
          <p className="flex gap-3">
            <b className="text-primary font-mono text-base">B</b>
            <span>Price deviation check & scam-pattern scan run in parallel.</span>
          </p>
          <p className="flex gap-3">
            <b className="text-primary font-mono text-base">C</b>
            <span>You receive a 0–100 Trust Score with plain-English red flags before contacting the seller.</span>
          </p>
        </div>
      </aside>
    </div>
  );
}
