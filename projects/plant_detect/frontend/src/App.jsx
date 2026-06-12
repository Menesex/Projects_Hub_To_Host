import { useState } from 'react'
import { identifyPlant } from './services/api'
import ImageUploader from './components/ImageUploader'
import PlantCard from './components/PlantCard'

function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [preview, setPreview] = useState(null)

  const handleImageUpload = async (file) => {
    setLoading(true)
    setError(null)
    setResult(null)
    
    // Crear una previsualización de la foto para el usuario
    setPreview(URL.createObjectURL(file))

    try {
      const response = await identifyPlant(file)
      if (response.success) {
        setResult(response.data)
      } else {
        setError("No pudimos identificar la planta.")
      }
    } catch (err) {
      setError("Error de conexión con el servidor.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <header className="max-w-md mx-auto text-center mb-8">
        <h1 className="text-3xl font-bold text-green-700">🌿 Bio AI</h1>
        <p className="text-gray-600">Identifica tus plantas al instante</p>
      </header>

      <main className="max-w-md mx-auto space-y-6">
        {/* Componente para subir/tomar foto */}
        <ImageUploader onUpload={handleImageUpload} loading={loading} />

        {/* Previsualización de la foto subida */}
        {preview && (
          <div className="rounded-xl overflow-hidden shadow-md">
            <img src={preview} alt="Preview" className="w-full h-48 object-cover" />
          </div>
        )}

        {/* Estado de carga */}
        {loading && (
          <div className="text-center p-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-700 mx-auto"></div>
            <p className="mt-4 text-green-700 font-medium">Analizando con IA...</p>
          </div>
        )}

        {/* Errores */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Resultados: Aquí recorremos la lista que manda tu Backend */}
        {result && result.is_plant && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-800">Resultados encontrados:</h2>
            {result.results.map((plant, index) => (
              <PlantCard key={index} plant={plant} isTopMatch={index === 0} />
            ))}
          </div>
        )}

        {result && !result.is_plant && (
          <div className="text-center p-8 bg-yellow-50 rounded-xl border border-yellow-200">
            <p className="text-yellow-700">⚠️ {result.message || "No parece ser una planta."}</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App