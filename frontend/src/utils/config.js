export const API_ROOT = import.meta.env.VITE_API_ROOT;

export function getApiUrl(path) {
    return `${API_ROOT}${path}`;
}