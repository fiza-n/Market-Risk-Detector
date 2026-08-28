import React from 'react';
import { ListingForm } from '../components/ListingForm.jsx';
import { ShieldCheck } from 'lucide-react';

export function SubmitPage({ onSubmitListing, loading }) {
  return (
    <section className="mx-auto max-w-6xl px-5 py-10 md:py-16">
      <div className="max-w-3xl mb-10">
        <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1.5 font-mono text-xs text-primary shadow-xs">
          <span className="size-2 rounded-full bg-emerald-600 animate-pulse" aria-hidden="true" />
          Pakistani Marketplace Scam Shield
        </div>

        <h1 className="text-4xl font-bold tracking-tight text-foreground md:text-6xl">
          What are you about to <span className="text-primary">buy?</span>
        </h1>
        <p className="mt-4 text-base text-muted-foreground leading-relaxed md:text-lg">
          Paste any listing from OLX Pakistan, Facebook Marketplace groups, or third-party sellers. Get an upfront 0–100 trust score and red flag analysis before investing time or money.
        </p>
      </div>

      <ListingForm onSubmit={onSubmitListing} loading={loading} />
    </section>
  );
}
