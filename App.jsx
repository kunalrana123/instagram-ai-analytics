import React, { useState } from 'react'
import axios from 'axios'
import './index.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [username, setUsername] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyzeProfile = async () => {
    if (!username.trim()) {
      setError('Please enter a username')
      return
    }

    setLoading(true)
    setError('')
    
    try {
      const response = await axios.post(`${API_BASE}/analyze-profile`, {
        username: username.trim(),
        posts_limit: 12
      })
      
      setAnalysis(response.data.analysis)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze profile')
    } finally {
      setLoading(false)
    }
  }

  const MetricCard = ({ title, value, color = "blue" }) => (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <p className={`text-2xl font-bold text-${color}-600 mt-2`}>{value}</p>
    </div>
  )

  const ColorPalette = ({ colors = [] }) => (
    <div className="flex space-x-2">
      {colors.slice(0, 5).map((color, index) => (
        <div
          key={index}
          className="w-8 h-8 rounded-full border-2 border-gray-200"
          style={{ backgroundColor: color }}
          title={color}
        />
      ))}
    </div>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Instagram AI Analytics
          </h1>
          <p className="text-gray-600 text-lg">
            Analyze Instagram profiles with AI-powered insights
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 mb-8">
          <div className="flex space-x-4">
            <input
              type="text"
              placeholder="Enter Instagram username (e.g., nasa)"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              onKeyPress={(e) => e.key === 'Enter' && analyzeProfile()}
            />
            <button
              onClick={analyzeProfile}
              disabled={loading}
              className="px-8 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-medium hover:from-purple-700 hover:to-pink-700 transition-colors disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
          {error && (
            <p className="text-red-600 text-sm mt-2">{error}</p>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto mb-4"></div>
            <h2 className="text-xl font-semibold text-gray-900">
              Analyzing Instagram Profile...
            </h2>
            <p className="text-gray-600 mt-2">
              Processing images, analyzing sentiment, and generating insights
            </p>
          </div>
        )}

        {/* Results */}
        {analysis && !loading && (
          <div className="space-y-8">
            {/* Overview Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <MetricCard 
                title="Followers" 
                value={analysis.profile?.followers?.toLocaleString() || 'N/A'} 
                color="blue" 
              />
              <MetricCard 
                title="Engagement Rate" 
                value={`${analysis.engagement?.engagement_rate || 0}%`} 
                color="green" 
              />
              <MetricCard 
                title="Brand Consistency" 
                value={`${analysis.branding?.consistency_score || 0}%`} 
                color="purple" 
              />
              <MetricCard 
                title="Sentiment Score" 
                value={`${Math.round((analysis.sentiment?.overall || 0) * 100)}%`} 
                color="pink" 
              />
            </div>

            {/* Brand Analysis */}
            {analysis.branding && (
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Brand Analysis</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Brand Alignment</h3>
                    <p className="text-lg text-purple-600 font-medium">
                      {analysis.branding.brand_alignment}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">
                      Consistency: {analysis.branding.consistency_score}%
                    </p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Color Palette</h3>
                    <ColorPalette colors={analysis.branding.dominant_colors} />
                    <p className="text-sm text-gray-600 mt-2">
                      Variance: {analysis.branding.color_variance}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Engagement & Sentiment */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {analysis.engagement && (
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Engagement</h2>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Average Likes:</span>
                      <span className="font-semibold">{analysis.engagement.avg_likes?.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Average Comments:</span>
                      <span className="font-semibold">{analysis.engagement.avg_comments?.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Trend:</span>
                      <span className={`font-semibold ${
                        analysis.engagement.trend === 'Increasing' ? 'text-green-600' : 
                        analysis.engagement.trend === 'Decreasing' ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {analysis.engagement.trend}
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {analysis.sentiment && (
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Sentiment</h2>
                  <div className="space-y-3">
                    <div>
                      <div className="flex justify-between mb-2">
                        <span className="text-gray-600">Overall Sentiment:</span>
                        <span className="font-semibold">{analysis.sentiment.emotional_tone}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-2 rounded-full"
                          style={{ width: `${Math.max(0, Math.min(100, (analysis.sentiment.overall + 1) * 50))}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Insights */}
            {analysis.insights && analysis.insights.length > 0 && (
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Key Insights</h2>
                <div className="space-y-3">
                  {analysis.insights.map((insight, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                      <p className="text-blue-800">{insight}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Mood Suggestions */}
            {analysis.mood_suggestions && analysis.mood_suggestions.length > 0 && (
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Brand Mood Suggestions</h2>
                <div className="space-y-3">
                  {analysis.mood_suggestions.map((suggestion, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-purple-50 rounded-lg">
                      <div className="w-2 h-2 bg-purple-500 rounded-full mt-2 flex-shrink-0"></div>
                      <p className="text-purple-800">{suggestion}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>Instagram AI Analytics - Powered by AI & Computer Vision</p>
        </div>
      </div>
    </div>
  )
}

export default App
