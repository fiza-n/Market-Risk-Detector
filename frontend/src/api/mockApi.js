/**
 * Mock API Layer for Marketplace Risk Detector
 * Implements exact JSON shapes specified in docs/Shared_Data_Contract.md
 */

export const CATEGORIES = [
  "Mobile Phones",
  "Electronics",
  "Vehicles",
  "Furniture",
  "Fashion",
  "Property/Rent",
  "Other"
];

export async function mockSubmitListing(listingData) {
  // Simulate network delay (800ms)
  await new Promise((resolve) => setTimeout(resolve, 800));

  const text = `${listingData.title || ''} ${listingData.description || ''} ${listingData.seller_info || ''}`.toLowerCase();
  const price = Number(listingData.price) || 0;
  const category = listingData.category || 'Mobile Phones';

  const flags = [];
  let scorePenalty = 0;

  // Pakistani market scam signal checks
  if (/advance|payment|jazzcash|easypaisa|bank transfer|deposit|pay first|advance payment|token money/i.test(text)) {
    flags.push("Advance payment pressure detected: Seller demands money via JazzCash/EasyPaisa/Bank before product inspection.");
    scorePenalty += 40;
  }

  if (/cod not available|no cod|delivery only|courier only/i.test(text)) {
    flags.push("No COD (Cash on Delivery) allowed: Seller explicitly refuses in-person handoff or COD.");
    scorePenalty += 20;
  }

  if (/urgent|shifting abroad|leaving country|emergency sale|only serious|final price|today only/i.test(text)) {
    flags.push("High urgency pressure: Seller creates artificial time pressure to bypass verification.");
    scorePenalty += 15;
  }

  if (/whatsapp|contact on whatsapp|03\d{9}/i.test(text)) {
    flags.push("Off-platform communication: Seller prompts buyer to leave marketplace chat immediately.");
    scorePenalty += 10;
  }

  if (/brand new|sealed pack|box packed/i.test(text) && price < 50000 && category === "Mobile Phones") {
    flags.push("Abnormally low price for claimed sealed item: Price deviates significantly from local market reference.");
    scorePenalty += 25;
  }

  if (listingData.seller_info && /2 days|new account|just joined|no rating/i.test(listingData.seller_info)) {
    flags.push("New seller account: Seller profile was created recently with no transaction history.");
    scorePenalty += 10;
  }

  if (flags.length === 0) {
    flags.push("No explicit scam patterns detected in listing text.");
  }

  const score = Math.max(12, Math.min(98, 100 - scorePenalty));

  let verdict = "low_risk";
  if (score < 40) {
    verdict = "high_risk";
  } else if (score < 70) {
    verdict = "medium_risk";
  }

  let tip = "Meet in a well-lit public place (e.g. inside a mall or bank) to inspect the item before paying.";
  if (verdict === "high_risk") {
    tip = "CRITICAL: Do NOT send any advance payment via JazzCash or EasyPaisa under any pretext. Insist on inspecting the item in person first.";
  } else if (verdict === "medium_risk") {
    tip = "CAUTION: Proceed with care. Verify physical possession of the item, test functionality, and avoid paying before inspection.";
  }

  const submission_id = `sub_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

  // Return Object #4 JSON contract
  return {
    submission_id,
    score,
    verdict,
    flags,
    tip
  };
}

export async function mockSubmitFeedback(feedbackData) {
  await new Promise((resolve) => setTimeout(resolve, 300));
  return {
    success: true,
    message: "Feedback recorded",
    submission_id: feedbackData.submission_id
  };
}

export async function mockFetchCategories() {
  return CATEGORIES;
}
