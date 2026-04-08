import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './Sidebar';
import Tasks from './Tasks';
import Residents from './Residents';
import Reports from './Reports';
import Knowledge from './Knowledge';
import Settings from './Settings';

function App() {
  return (
    <Router>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 p-6">
          <Routes>
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/residents" element={<Residents />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/knowledge" element={<Knowledge />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
