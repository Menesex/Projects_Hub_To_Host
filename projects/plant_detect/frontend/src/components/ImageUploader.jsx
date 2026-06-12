export default function ImageUploader({ onUpload, loading }) {
  const handleChange = (e) => {
    const file = e.target.files[0]
    if (file) onUpload(file)
  }

  return (
    <div className="relative">
      <label className={`
        flex flex-col items-center justify-center w-full h-32 
        border-2 border-dashed rounded-xl cursor-pointer
        ${loading ? 'bg-gray-100 border-gray-300' : 'bg-white border-green-300 hover:bg-green-50'}
        transition-colors duration-200
      `}>
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          <span className="text-3xl mb-2">📸</span>
          <p className="text-sm text-gray-500 font-medium">
            {loading ? "Procesando..." : "Toca para tomar foto o subir"}
          </p>
        </div>
        <input 
          type="file" 
          className="hidden" 
          accept="image/*" 
          capture="environment" // Esto fuerza a abrir la cámara trasera en móviles
          onChange={handleChange}
          disabled={loading}
        />
      </label>
    </div>
  )
}