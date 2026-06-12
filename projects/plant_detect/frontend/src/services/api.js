const API_URL = "https://plantdetectyourself.onrender.com/api"; // commit con mi cuenta para que vercel no me chimbeeee

export const identifyPlant = async (imageFile) => {
    const formData = new FormData();
    formData.append("file", imageFile);

    try {
    const response = await fetch(`${API_URL}/identify?lang=es`, {
        method: "POST",
        body: formData,
      // No necesitas poner Content-Type, el navegador lo pone solo para FormData
    });

    if (!response.ok) throw new Error("Error en la identificación");
    
    return await response.json();
    } catch (error) {
    console.error("API Error:", error);
    throw error;
    }
};