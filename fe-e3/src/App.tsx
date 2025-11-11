import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from './components/layout/Layout'
import Test from './pages/Test'
import Agents from './pages/Agents'
import Drivers from './pages/Drivers'
import Conversations from './pages/Conversations'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/test" replace />} />
        <Route path="/test" element={<Test />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/drivers" element={<Drivers />} />
        <Route path="/conversations" element={<Conversations />} />
      </Routes>
    </Layout>
  )
}

export default App
