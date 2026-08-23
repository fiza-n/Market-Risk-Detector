import React, { useState } from 'react';
import { Copy, Check, Share2 } from 'lucide-react';

export function ShareCard({ result, listing }) {
  const [copied, setCopied] = useState(false);

  if (!result || !listing) return null;

  const handleCopy = () => {
    const textToCopy = `🛡️ Marketplace Risk Detector Result\n📌 Listing: "${listing.title || 'Marketplace Item'}"\n💰 Price: PKR ${listing.price || 'N/A'}\n📊 Trust Score: ${result.score}/100 (${(result.verdict || '').replace('_', ' ').toUpperCase()})\n\n💡 Tip: ${result.tip || 'Inspect item before paying'}\n\nCheck Pakistani listings before you pay at safespot.pk!`;
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(textToCopy);
    } else {
      // Fallback
      const textarea = document.createElement('textarea');
      textarea.value = textToCopy;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    }

    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="mt-8 flex flex-col gap-5 rounded-3xl bg-[#183f3a] p-7 text-[#f7f5f0] md:flex-row md:items-center md:justify-between shadow-lg">
      <div>
        <div className="flex items-center gap-2 text-[#f2b35b]">
          <Share2 size={16} />
          <span className="font-mono text-xs uppercase tracking-[.18em] font-semibold">Shareable Result Card</span>
        </div>
        <h2 className="mt-2 text-2xl font-bold tracking-tight text-white">Help someone pause before they pay.</h2>
        <p className="mt-1 text-xs text-emerald-100/80">
          Share this trust signal card with friends, family, or on Product Hunt & WhatsApp.
        </p>
      </div>

      <button
        onClick={handleCopy}
        className="rounded-xl bg-[#f2b35b] px-6 py-3.5 font-bold text-[#183f3a] hover:bg-[#f2b35b]/90 transition-all flex items-center justify-center gap-2 shrink-0 shadow-md"
      >
        {copied ? (
          <>
            <Check size={18} /> Copied to Clipboard
          </>
        ) : (
          <>
            <Copy size={18} /> Copy Share Card Text
          </>
        )}
      </button>
    </div>
  );
}
