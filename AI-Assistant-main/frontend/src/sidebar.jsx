import { NavLink } from 'react-router-dom';  // 1. Import NavLink

// 2. Define the navLinkClass function
const navLinkClass = ({ isActive }) =>
  isActive
    ? "block py-2 px-4 rounded bg-gradient-to-r from-blue-500 to-blue-700 text-white font-bold shadow-md"
    : "block py-2 px-4 rounded hover:bg-gray-700 transition-all duration-200";

const Sidebar = () => {   // 3. Sidebar component
  return (
    <div className="w-64 h-screen bg-gray-800 text-white flex flex-col shadow-lg">
      <h1 className="text-2xl font-bold p-4 border-b border-gray-700">Dashboard</h1>
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          <li><NavLink to="/tasks" className={navLinkClass}>Tasks</NavLink></li>
          <li><NavLink to="/residents" className={navLinkClass}>Residents</NavLink></li>
          <li><NavLink to="/reports" className={navLinkClass}>Reports</NavLink></li>
          <li><NavLink to="/knowledge" className={navLinkClass}>Knowledge</NavLink></li>
          <li><NavLink to="/settings" className={navLinkClass}>Settings</NavLink></li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;  // 4. Export Sidebar
