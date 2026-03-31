import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/index.jsx'

// Public pages
import LandingPage  from './pages/LandingPage'
import EventForm    from './pages/EventForm'
import SuccessPage  from './pages/SuccessPage'
import Datenschutz  from './pages/Datenschutz'

// Admin pages
import AdminLogin        from './pages/admin/AdminLogin'
import AdminDashboard    from './pages/admin/AdminDashboard'
import AdminEventDetail  from './pages/admin/AdminEventDetail'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* ── Öffentliche Routen ── */}
          <Route path="/"              element={<LandingPage />} />
          <Route path="/formular/:eventId" element={<EventForm />} />
          <Route path="/erfolg"        element={<SuccessPage />} />
          <Route path="/datenschutz"   element={<Datenschutz />} />

          {/* ── Admin-Routen (geschützt) ── */}
          <Route path="/admin/login"   element={<AdminLogin />} />
          <Route
            path="/admin"
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/veranstaltung/:eventId"
            element={
              <ProtectedRoute>
                <AdminEventDetail />
              </ProtectedRoute>
            }
          />

          {/* ── Fallback ── */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
