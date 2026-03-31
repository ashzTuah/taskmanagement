const API_URL = process.env.REACT_APP_API_URL;

export const getToken = () => localStorage.getItem("token");

export const apiFetch = async (url, options = {}) => {
  const token = getToken();

  const res = await fetch(`${API_URL}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    }
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
    return;
  }

  // return res.json();
  const text = await res.text();
  try {
    return text ? JSON.parse(text) : null;
  } catch (err) {
    console.error("Failed to parse JSON:", err);
    return null;
  }
};