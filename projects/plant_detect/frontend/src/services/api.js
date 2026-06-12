// Dynamic API URL - works in both development and production
const getAPIUrl = () => {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000/api/plants';
  }
  return 'https://mene-project-portfolio.onrender.com/api/plants';
};

const API_URL = getAPIUrl();

export const identifyPlant = async (imageFile) => {
    const formData = new FormData();
    formData.append("file", imageFile);

    try {
    const response = await fetch(`${API_URL}/identify?lang=es`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) throw new Error("Error en la identificación");

    return await response.json();
    } catch (error) {
    console.error("API Error:", error);
    throw error;
    }
};