import React from 'react';
import { ResultCard } from '../components/ResultCard.jsx';
import { FeedbackButtons } from '../components/FeedbackButtons.jsx';
import { ShareCard } from '../components/ShareCard.jsx';
import { ArrowLeft, RefreshCw } from 'lucide-react';

export function ResultPage({ result, listing, onReset }) {
  if (!result) return null;

  return (
    <section className="mx-auto max-w-6xl px-5 py-10 md:py-16">
      {/* Top Bar */}
      <div className="flex flex-wrap items-end justify-between gap-5 mb-10 pb-6 border-b border-border">
        <div>
          <p className="font-mono text-xs uppercase tracking-[.18em] text-primary font-bold">
            Analysis Complete / Risk Assessment Report
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight text-foreground md:text-5xl">
            Your Second Opinion.
          </h1>
          {listing?.title && (
            <p className="mt-1 text-sm text-muted-foreground truncate max-w-xl">
              Analyzed: <span className="font-medium text-foreground">"{listing.title}"</span>
            </p>
          )}
        </div>

        <button
          onClick={onReset}
          className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-5 py-2.5 text-xs font-bold text-foreground hover:bg-muted transition-colors shadow-xs"
        >
          <RefreshCw size={14} /> Check Another Listing
        </button>
      </div>

      {/* Result Card */}
      <ResultCard result={result} />

      {/* Accuracy Feedback */}
      <FeedbackButtons submissionId={result.submission_id} />

      {/* Share Card */}
      <ShareCard result={result} listing={listing} />
    </section>
  );
}
