const API_URL = process.env.REACT_APP_API_URL;

export const getToken = () => localStorage.getItem("token");

export const apiFetch = async (url, options = {}) => {
  const token = getToken();

  const res = await fetch(`${API_URL}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` })
    }
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }

  return res.json();
};