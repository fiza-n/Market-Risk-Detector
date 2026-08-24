import {
  mockSubmitListing,
  mockSubmitFeedback,
  mockFetchCategories,
  CATEGORIES
} from './mockApi.js';

// Set FORCE_MOCK = true by default for standalone frontend dev to avoid ECONNREFUSED proxy logs when backend is offline
const FORCE_MOCK = false;
const API_BASE_URL = '/api';

/**
 * Submit listing for risk analysis
 * @param {Object} listingData - { title, description, price, category, seller_info }
 * @returns {Promise<Object>} - Object #4: { submission_id, score, verdict, flags, tip }
 */
export async function submitListing(listingData) {
  if (FORCE_MOCK) {
    return await mockSubmitListing(listingData);
  }

  try {
    const response = await fetch(`${API_BASE_URL}/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: listingData.title || '',
        description: listingData.description || '',
        price: Number(listingData.price) || 0,
        category: listingData.category || CATEGORIES[0],
        seller_info: listingData.seller_info || null,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.warn('Backend server offline. Using mock API fallback.');
    return await mockSubmitListing(listingData);
  }
}

/**
 * Submit feedback vote for a submission
 * @param {Object} feedbackData - { submission_id, was_accurate }
 * @returns {Promise<Object>} - { success: true }
 */
export async function submitFeedback(feedbackData) {
  if (FORCE_MOCK) {
    return await mockSubmitFeedback(feedbackData);
  }

  try {
    const response = await fetch(`${API_BASE_URL}/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        submission_id: feedbackData.submission_id,
        was_accurate: Boolean(feedbackData.was_accurate),
        submitted_at: new Date().toISOString(),
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.warn('Backend server offline. Using mock feedback fallback.');
    return await mockSubmitFeedback(feedbackData);
  }
}

/**
 * Fetch available listing categories
 * @returns {Promise<Array<string>>}
 */
export async function fetchCategories() {
  if (FORCE_MOCK) {
    return await mockFetchCategories();
  }

  try {
    const response = await fetch(`${API_BASE_URL}/meta/categories`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.categories || CATEGORIES;
  } catch (error) {
    console.warn('Backend server offline. Using default categories list fallback.');
    return await mockFetchCategories();
  }
}
