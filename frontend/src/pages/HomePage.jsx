import React from 'react';
import { ArrowRight, Sparkles } from 'lucide-react';

export function HomePage({ onStartChecking, onNavigateToHowItWorks }) {
  return (
    <>
      {/* Hero Section */}
      <section className="mx-auto grid max-w-6xl gap-12 px-5 pb-20 pt-16 md:grid-cols-[1.1fr_.9fr] md:items-center md:pt-24">
        <div>
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-card px-3.5 py-1.5 font-mono text-xs text-primary shadow-xs">
            <span className="size-2 rounded-full bg-emerald-600 animate-pulse" />
            Built for buyers in Pakistan
          </div>

          <h1 className="max-w-3xl text-balance text-5xl font-bold leading-[1.05] tracking-[-.04em] text-foreground md:text-7xl">
            Pause before you <span className="text-primary">pay.</span>
          </h1>

          <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted-foreground">
            Paste any OLX, Facebook Marketplace, or Daraz listing. Get an upfront 0–100 trust score and plain-English red flags before sharing your phone number or sending advance money.
          </p>

          <div className="mt-9 flex flex-wrap items-center gap-4">
            <button
              onClick={onStartChecking}
              className="rounded-full bg-primary px-7 py-4 font-bold text-primary-foreground shadow-lg shadow-primary/15 hover:bg-primary/90 transition-all flex items-center gap-2 text-base"
            >
              Check a Listing <ArrowRight size={18} />
            </button>

            <button
              onClick={onNavigateToHowItWorks}
              className="rounded-full border border-border bg-card px-6 py-4 font-bold text-foreground hover:bg-muted transition-all text-sm"
            >
              How It Works
            </button>
          </div>
        </div>

        {/* Visual Live Scan Card Preview (v0 Reference Reimplementation) */}
        <div className="relative rounded-[2rem] bg-primary p-7 text-primary-foreground md:rotate-2 md:p-9 shadow-xl border border-primary/20">
          <div className="flex items-center justify-between border-b border-primary-foreground/20 pb-5">
            <span className="font-mono text-xs uppercase tracking-[.18em] text-primary-foreground/80 font-bold">
              Live Scan Mockup / 02
            </span>
            <Sparkles size={20} className="text-accent" />
          </div>

          <div className="py-8">
            <div className="font-mono text-7xl font-bold tracking-tight text-white">
              42<span className="text-3xl font-mono text-primary-foreground/75">/100</span>
            </div>
            <p className="mt-3 text-2xl font-bold text-white">Proceed Carefully</p>
            <p className="mt-2 max-w-xs text-xs leading-5 text-primary-foreground/80">
              Advance payment pressure detected. Seller demands JazzCash/EasyPaisa before physical inspection.
            </p>
          </div>

          <div className="flex flex-wrap gap-2 text-xs font-mono pt-2">
            <span className="rounded-full bg-accent px-3 py-1.5 font-bold text-accent-foreground">
              2 Red Flags
            </span>
            <span className="rounded-full border border-primary-foreground/30 px-3 py-1.5 text-primary-foreground/90">
              Pattern Scan Complete
            </span>
          </div>
        </div>
      </section>

      {/* 3 Step Process Strip */}
      <section className="border-y border-border bg-secondary/80">
        <div className="mx-auto grid max-w-6xl gap-8 px-5 py-12 md:grid-cols-3">
          <div className="flex flex-col justify-between">
            <div>
              <p className="font-mono text-xs font-bold text-primary tracking-wider uppercase">01 / BEFORE CONTACT</p>
              <h3 className="mt-2 text-xl font-bold text-foreground">See the signals early.</h3>
              <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
                Know whether a seller demands JazzCash/EasyPaisa or refuses COD before giving away your WhatsApp number.
              </p>
            </div>
          </div>

          <div className="flex flex-col justify-between">
            <div>
              <p className="font-mono text-xs font-bold text-primary tracking-wider uppercase">02 / PLAIN ENGLISH</p>
              <h3 className="mt-2 text-xl font-bold text-foreground">Know what to verify.</h3>
              <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
                Clear, actionable advice on item physical testing, price deviation against local market reference data.
              </p>
            </div>
          </div>

          <div className="flex flex-col justify-between">
            <div>
              <p className="font-mono text-xs font-bold text-primary tracking-wider uppercase">03 / COMMUNITY LOOP</p>
              <h3 className="mt-2 text-xl font-bold text-foreground">Make detection sharper.</h3>
              <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
                Buyer accuracy feedback votes train our scam detection models to keep Pakistani buyers protected.
              </p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
