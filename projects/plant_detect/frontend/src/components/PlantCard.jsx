export default function PlantCard({ plant, isTopMatch }) {
  return (
    <div className={`
      bg-white rounded-2xl shadow-sm border overflow-hidden
      ${isTopMatch ? 'border-green-500 ring-1 ring-green-500' : 'border-gray-200'}
    `}>
      <div className="p-5">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-lg font-bold text-gray-900">{plant.common_name}</h3>
          <span className="bg-green-100 text-green-800 text-xs font-bold px-2.5 py-0.5 rounded-full">
            {plant.confidence_percentage}%
          </span>
        </div>
        
        <p className="italic text-sm text-gray-500 mb-3">{plant.scientific_name}</p>
        <p className="text-gray-700 text-sm mb-4 leading-relaxed">{plant.description}</p>

        <div className="space-y-3">
          <div>
            <h4 className="text-xs font-bold uppercase text-gray-400 tracking-wider mb-1">Cuidados</h4>
            <ul className="grid grid-cols-1 gap-1">
              {plant.care_tips.map((tip, i) => (
                <li key={i} className="text-sm text-gray-600 flex items-start">
                  <span className="mr-2 text-green-500">•</span> {tip}
                </li>
              ))}
            </ul>
          </div>

          <div className="flex gap-4 pt-2">
            <div>
              <h4 className="text-xs font-bold uppercase text-gray-400 mb-1">Toxicidad</h4>
              <p className={`text-xs font-medium px-2 py-1 rounded ${
                plant.toxicity.toLowerCase().includes('safe') ? 'bg-blue-50 text-blue-700' : 'bg-red-50 text-red-700'
              }`}>
                {plant.toxicity}
              </p>
            </div>
            <div>
              <h4 className="text-xs font-bold uppercase text-gray-400 mb-1">Origen</h4>
              <p className="text-xs text-gray-600 font-medium">{plant.origin}</p>
            </div>
          </div>
          
          <div className="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-100">
            <p className="text-xs text-yellow-800 italic"><strong>Dato curioso:</strong> {plant.fun_fact}</p>
          </div>
        </div>
      </div>
    </div>
  )
}