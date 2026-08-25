import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown, CheckCircle2 } from 'lucide-react';
import { submitFeedback } from '../api/client.js';

export function FeedbackButtons({ submissionId }) {
  const [selectedVote, setSelectedVote] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleVote = async (wasAccurate) => {
    if (isSubmitting || submitted) return;

    setSelectedVote(wasAccurate ? 'up' : 'down');
    setIsSubmitting(true);

    try {
      await submitFeedback({
        submission_id: submissionId || `sub_local_${Date.now()}`,
        was_accurate: wasAccurate,
      });
      setSubmitted(true);
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mt-6 flex flex-col items-start justify-between gap-4 rounded-3xl bg-secondary p-6 sm:flex-row sm:items-center border border-border">
      <div>
        <h3 className="font-bold text-foreground text-base">Was this assessment helpful/accurate?</h3>
        <p className="mt-0.5 text-xs text-muted-foreground">
          Your feedback sharpens pattern detection for future Pakistani marketplace buyers.
        </p>
      </div>

      <div className="flex items-center gap-3">
        {submitted ? (
          <div className="inline-flex items-center gap-2 rounded-xl bg-primary/10 border border-primary/20 px-4 py-2 text-xs font-bold text-primary">
            <CheckCircle2 size={16} />
            Thanks for your feedback
          </div>
        ) : (
          <>
            <button
              onClick={() => handleVote(true)}
              disabled={isSubmitting}
              aria-label="Yes, this assessment was helpful and accurate"
              className={`flex items-center gap-2 rounded-xl border px-4 py-2.5 text-xs font-bold transition-all ${
                selectedVote === 'up'
                  ? 'bg-primary text-primary-foreground border-primary'
                  : 'bg-background hover:bg-muted text-foreground border-input'
              }`}
            >
              <ThumbsUp size={16} />
              Yes
            </button>

            <button
              onClick={() => handleVote(false)}
              disabled={isSubmitting}
              aria-label="No, this assessment was not helpful or accurate"
              className={`flex items-center gap-2 rounded-xl border px-4 py-2.5 text-xs font-bold transition-all ${
                selectedVote === 'down'
                  ? 'bg-accent text-accent-foreground border-accent'
                  : 'bg-background hover:bg-muted text-foreground border-input'
              }`}
            >
              <ThumbsDown size={16} />
              No
            </button>
          </>
        )}
      </div>
    </div>
  );
}
