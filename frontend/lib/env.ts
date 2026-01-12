export const getRecommendBaseUrl = () => {
  const envUrl = process.env.NEXT_PUBLIC_RECOMMEND_API_URL;

  if (typeof window !== 'undefined') {
    if (envUrl && !envUrl.includes('recommendation-service')) return envUrl;
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:8001`;
  }

  return envUrl || 'http://recommendation-service:8001';
};
