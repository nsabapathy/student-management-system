import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import StudentList from './components/StudentList'
import StudentForm from './components/StudentForm'
import Login from './components/Login'
import Register from './components/Register'
import ProtectedRoute from './components/ProtectedRoute'
import './App.css'

function App() {
  // Check if user is logged in
  const isLoggedIn = localStorage.getItem('token') !== null;

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        {isLoggedIn && (
          <nav className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex">
                  <div className="flex-shrink-0 flex items-center">
                    <Link to="/" className="text-xl font-bold text-gray-800">
                      Student Management
                    </Link>
                  </div>
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    <Link
                      to="/students"
                      className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                    >
                      Students
                    </Link>
                  </div>
                </div>
                <div className="flex items-center">
                  <button
                    onClick={() => {
                      // Clear authentication data
                      localStorage.removeItem('token');
                      // Redirect to login
                      window.location.href = '/login';
                    }}
                    className="bg-red-500 hover:bg-red-700 text-white py-1 px-3 rounded-md text-sm"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </nav>
        )}

        <main>
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <Routes>
              {/* Public routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              
              {/* Protected routes */}
              <Route element={<ProtectedRoute />}>
                <Route path="/" element={<StudentList />} />
                <Route path="/students" element={<StudentList />} />
                <Route path="/students/new" element={<StudentForm />} />
                <Route path="/students/:id/edit" element={<StudentForm />} />
              </Route>
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App
