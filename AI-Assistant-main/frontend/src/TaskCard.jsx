const TaskCard = ({ name, status, action, unit, phone, badge }) => {
    const statusColors = {
      "New Lead": "bg-blue-500",
      "Application Sent": "bg-yellow-500",
      "Tour Scheduled": "bg-purple-500",
      "Lease Signed": "bg-green-500",
    };
  
    const badgeColors = {
      "Prospect": "bg-purple-500",
      "Current": "bg-green-500",
      "Future": "bg-blue-500",
    };
  
    return (
      <div className="bg-white rounded-lg shadow-md p-4 mb-4 flex flex-col gap-3 hover:shadow-xl hover:scale-[1.02] transition-all duration-300">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-gray-800">{name}</h3>
            {badge && (
              <span className={`text-xs font-semibold text-white py-1 px-2 rounded-full ${badgeColors[badge] || 'bg-gray-400'}`}>
                {badge}
              </span>
            )}
          </div>
          <span className={`text-xs font-semibold text-white py-1 px-2 rounded ${statusColors[status] || 'bg-gray-400'}`}>
            {status}
          </span>
        </div>
  
        <div className="text-sm text-gray-600">
          <p><span className="font-semibold">Unit:</span> {unit}</p>
          <p><span className="font-semibold">Phone:</span> {phone}</p>
        </div>
  
        <button className="mt-2 bg-blue-500 text-white text-sm font-semibold py-1 px-3 rounded hover:bg-blue-600 transition self-start">
          {action}
        </button>
      </div>
    );
  };
  
  export default TaskCard;
  