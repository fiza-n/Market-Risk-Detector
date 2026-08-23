import React from 'react';
import { ShieldCheck, TriangleAlert, Check, CircleAlert, Lightbulb } from 'lucide-react';

export function ResultCard({ result }) {
  if (!result) return null;

  const { score = 50, verdict = 'medium_risk', flags = [], tip = '' } = result;

  const isHighRisk = verdict === 'high_risk' || score < 40;
  const isMediumRisk = verdict === 'medium_risk' || (score >= 40 && score < 70);

  const getVerdictLabel = () => {
    if (isHighRisk) return 'High Risk';
    if (isMediumRisk) return 'Medium Risk — Proceed Carefully';
    return 'Low Risk — Standard Precautions';
  };

  const getBadgeColor = () => {
    if (isHighRisk) return 'bg-accent text-accent-foreground border-accent';
    if (isMediumRisk) return 'bg-amber-100 text-amber-900 border-amber-300';
    return 'bg-emerald-100 text-emerald-900 border-emerald-300';
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[.85fr_1.15fr]">
      {/* Left Column: Trust Score Gauge */}
      <div className="rounded-3xl bg-primary p-7 text-primary-foreground md:p-9 shadow-md flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between border-b border-primary-foreground/20 pb-4">
            <span className="font-mono text-xs uppercase tracking-[.18em] opacity-80">Trust Score</span>
            <ShieldCheck size={26} className="text-accent" />
          </div>

          <div className="mt-8 font-mono text-8xl font-bold tracking-[-.08em] leading-none">
            {score}
            <span className="text-3xl font-mono tracking-normal opacity-70">/100</span>
          </div>

          <div className={`mt-6 inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-bold shadow-sm ${getBadgeColor()}`}>
            {isHighRisk ? <TriangleAlert size={16} /> : isMediumRisk ? <CircleAlert size={16} /> : <Check size={16} />}
            {getVerdictLabel()}
          </div>
        </div>

        <p className="mt-8 border-t border-primary-foreground/20 pt-5 text-xs leading-5 text-primary-foreground/75">
          Trust scores are an algorithmic risk signal based on price deviation and Pakistani scam patterns, not a financial guarantee. Always verify items in person before paying.
        </p>
      </div>

      {/* Right Column: Red Flags Breakdown & Tip */}
      <div className="rounded-3xl border border-border bg-card p-7 md:p-9 shadow-sm flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between pb-4 border-b border-border">
            <div>
              <h2 className="text-2xl font-bold text-foreground">Listing Risk Breakdown</h2>
              <p className="mt-1 text-xs text-muted-foreground">
                {flags.length} signal{flags.length === 1 ? '' : 's'} identified from listing analysis
              </p>
            </div>
            <CircleAlert className="text-primary" size={24} />
          </div>

          <div className="mt-6 flex flex-col gap-4">
            {flags.map((flag, index) => {
              // Parse title and detail if flag contains a colon or formatting
              const parts = flag.split(':');
              const flagTitle = parts.length > 1 ? parts[0].trim() : `Signal #${index + 1}`;
              const flagDetail = parts.length > 1 ? parts.slice(1).join(':').trim() : flag;

              return (
                <div key={index} className="flex gap-4 border-b border-border/60 pb-4 last:border-0 last:pb-0">
                  <span className={`mt-1 grid size-7 shrink-0 place-items-center rounded-full text-xs font-bold ${
                    isHighRisk ? 'bg-amber-100 text-amber-900 font-mono' : 'bg-secondary text-primary font-mono'
                  }`}>
                    {index + 1}
                  </span>
                  <div>
                    <h3 className="font-bold text-sm text-foreground">{flagTitle}</h3>
                    <p className="mt-1 text-xs leading-5 text-muted-foreground">{flagDetail}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Actionable Safety Tip Callout */}
        {tip && (
          <div className="mt-6 rounded-2xl bg-secondary/70 p-4 border border-border/80 flex gap-3 items-start">
            <Lightbulb size={20} className="text-primary shrink-0 mt-0.5" />
            <div>
              <strong className="block text-xs font-bold text-primary uppercase tracking-wider">Buyer Action Tip</strong>
              <p className="mt-1 text-xs leading-5 text-foreground/90 font-medium">{tip}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
