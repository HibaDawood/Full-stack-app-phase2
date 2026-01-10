// Function to safely decode base64
const base64Decode = (str: string): string => {
  // Replace URL-safe base64 chars to standard base64 chars
  str = str.replace(/-/g, '+').replace(/_/g, '/');

  // Pad with '=' if needed
  while (str.length % 4) {
    str += '=';
  }

  try {
    // Decode base64 to string
    return atob(str);
  } catch (error) {
    console.error('Error decoding base64:', error);
    return '';
  }
};

// Function to check if the token is expired
export const isTokenExpired = (token: string | null): boolean => {
  if (!token) return true;

  try {
    // Split the token to get the payload
    const parts = token.split('.');
    if (parts.length !== 3) return true;

    // Decode the payload (second part) - note: this is not secure, just for checking expiration
    const payload = base64Decode(parts[1]);
    if (!payload) return true;

    const payloadObj = JSON.parse(payload);

    // Check if token is expired
    const currentTime = Math.floor(Date.now() / 1000);
    return payloadObj.exp < currentTime;
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true;
  }
};

// Function to get a valid token
export const getValidToken = async (): Promise<string | null> => {
  const token = localStorage.getItem('auth_token');

  if (!token) {
    return null;
  }

  // Check if the token is still valid
  if (!isTokenExpired(token)) {
    return token;
  }

  // Token is expired, user needs to log in again
  return null;
};