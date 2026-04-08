import TaskCard from './TaskCard';

const Tasks = () => {
  const tasks = [
    { name: 'John Doe', status: 'New Lead', action: 'Reply Now', unit: '101A', phone: '555-123-4567', badge: 'Prospect' },
    { name: 'Jane Smith', status: 'Application Sent', action: 'Review App', unit: '202B', phone: '555-987-6543', badge: 'Future' },
    { name: 'Alex Johnson', status: 'Tour Scheduled', action: 'Confirm Tour', unit: '303C', phone: '555-321-9876', badge: 'Current' },
    { name: 'Emily Davis', status: 'Lease Signed', action: 'Welcome Email', unit: '404D', phone: '555-654-3210', badge: 'Current' },
  ];

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Tasks</h2>
      <div className="flex flex-col gap-4">
        {tasks.map((task, index) => (
          <TaskCard 
            key={index}
            name={task.name}
            status={task.status}
            action={task.action}
            unit={task.unit}
            phone={task.phone}
            badge={task.badge}
          />
        ))}
      </div>
    </div>
  );
};

export default Tasks;
