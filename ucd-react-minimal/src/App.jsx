import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import RegisterTeacher from './pages/RegisterTeacher';
import Login from './pages/Login';
import TeacherDashboard from './pages/TeacherDashboard';
import AddChild from './pages/AddChild';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register-teacher" element={<RegisterTeacher />} />
        <Route path="/login" element={<Login />} />
        <Route path="/add-child" element={<AddChild />} />
        <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
