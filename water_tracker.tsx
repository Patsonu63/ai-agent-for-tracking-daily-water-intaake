import { useState, useEffect } from 'react';
import { Droplet, Plus, Minus, RotateCcw, Award } from 'lucide-react';

export default function WaterIntakeTracker() {
  const [goal, setGoal] = useState(2000); // Default goal in ml
  const [intake, setIntake] = useState(0);
  const [log, setLog] = useState([]);
  const [history, setHistory] = useState([]);
  
  // Load data from localStorage on mount
  useEffect(() => {
    const savedData = localStorage.getItem('waterTrackerData');
    if (savedData) {
      const parsedData = JSON.parse(savedData);
      setGoal(parsedData.goal || 2000);
      
      // Check if we need to reset for a new day
      const lastDate = parsedData.lastUpdated ? new Date(parsedData.lastUpdated) : null;
      const today = new Date();
      
      if (!lastDate || lastDate.toDateString() !== today.toDateString()) {
        // New day - reset intake but keep history
        if (parsedData.intake > 0) {
          setHistory([...parsedData.history || [], {
            date: lastDate?.toDateString() || 'Previous day',
            intake: parsedData.intake,
            goal: parsedData.goal
          }]);
        }
        setIntake(0);
        setLog([]);
      } else {
        // Same day - restore data
        setIntake(parsedData.intake || 0);
        setLog(parsedData.log || []);
        setHistory(parsedData.history || []);
      }
    }
  }, []);
  
  // Save data to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('waterTrackerData', JSON.stringify({
      goal,
      intake,
      log,
      history,
      lastUpdated: new Date().toISOString()
    }));
  }, [goal, intake, log, history]);
  
  const addWater = (amount) => {
    const newIntake = intake + amount;
    setIntake(newIntake);
    
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    setLog([...log, {
      time: timeString,
      amount,
      total: newIntake
    }]);
  };
  
  const decreaseWater = (amount) => {
    if (intake - amount >= 0) {
      const newIntake = intake - amount;
      setIntake(newIntake);
      
      const now = new Date();
      const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      
      setLog([...log, {
        time: timeString,
        amount: -amount,
        total: newIntake
      }]);
    }
  };
  
  const resetDay = () => {
    if (intake > 0) {
      const today = new Date().toDateString();
      setHistory([...history, {
        date: today,
        intake,
        goal
      }]);
    }
    setIntake(0);
    setLog([]);
  };
  
  const progress = Math.min((intake / goal) * 100, 100);
  
  return (
    <div className="flex flex-col p-6 max-w-md mx-auto bg-blue-50 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-blue-800 mb-4 text-center">Water Intake Tracker</h2>
      
      {/* Current Date */}
      <div className="text-center mb-4 text-blue-600 font-medium">
        {new Date().toDateString()}
      </div>
      
      {/* Progress Section */}
      <div className="flex flex-col items-center mb-6">
        <div className="relative w-48 h-48 mb-4">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="relative w-36 h-36 bg-white rounded-full shadow-inner flex items-center justify-center overflow-hidden">
              <div 
                className="absolute bottom-0 left-0 right-0 bg-blue-400 transition-all duration-500 ease-in-out"
                style={{ height: `${progress}%`, opacity: 0.8 }}
              ></div>
              <div className="relative flex flex-col items-center">
                <Droplet className="text-blue-500 mb-1" size={28} />
                <span className="text-2xl font-bold text-blue-800">{intake} ml</span>
                <span className="text-sm text-blue-600">of {goal} ml</span>
              </div>
            </div>
          </div>
          <svg className="w-full h-full" viewBox="0 0 100 100">
            <circle 
              cx="50" cy="50" r="45" 
              fill="none" 
              stroke="#e6effd" 
              strokeWidth="8" 
            />
            <circle 
              cx="50" cy="50" r="45" 
              fill="none" 
              stroke="#3b82f6" 
              strokeWidth="8" 
              strokeDasharray={`${progress * 2.83} 283`}
              strokeLinecap="round"
              transform="rotate(-90 50 50)"
            />
          </svg>
        </div>
        <div className="text-center mt-2">
          <span className="text-lg font-semibold text-blue-700">
            {progress >= 100 ? (
              <div className="flex items-center">
                <Award className="text-yellow-500 mr-2" size={20} />
                Goal reached!
              </div>
            ) : (
              `${Math.round(progress)}% of daily goal`
            )}
          </span>
        </div>
      </div>
      
      {/* Water Controls */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="col-span-2 flex justify-between items-center mb-2">
          <span className="text-blue-800 font-medium">Daily Goal (ml):</span>
          <div className="flex items-center">
            <button 
              className="bg-blue-100 text-blue-700 rounded-l-md px-3 py-1 hover:bg-blue-200"
              onClick={() => setGoal(Math.max(goal - 250, 250))}
            >
              <Minus size={16} />
            </button>
            <span className="bg-white px-4 py-1 border-t border-b border-blue-200">{goal}</span>
            <button 
              className="bg-blue-100 text-blue-700 rounded-r-md px-3 py-1 hover:bg-blue-200"
              onClick={() => setGoal(goal + 250)}
            >
              <Plus size={16} />
            </button>
          </div>
        </div>
        
        <button 
          className="bg-blue-600 text-white rounded-lg p-3 flex items-center justify-center hover:bg-blue-700"
          onClick={() => addWater(250)}
        >
          <Droplet size={18} className="mr-2" />
          Add 250ml
        </button>
        
        <button 
          className="bg-blue-500 text-white rounded-lg p-3 flex items-center justify-center hover:bg-blue-600"
          onClick={() => addWater(500)}
        >
          <Droplet size={18} className="mr-2" />
          Add 500ml
        </button>
        
        <button 
          className="bg-blue-400 text-white rounded-lg p-3 flex items-center justify-center hover:bg-blue-500"
          onClick={() => decreaseWater(250)}
        >
          <Minus size={18} className="mr-2" />
          Remove 250ml
        </button>
        
        <button 
          className="bg-red-400 text-white rounded-lg p-3 flex items-center justify-center hover:bg-red-500"
          onClick={resetDay}
        >
          <RotateCcw size={18} className="mr-2" />
          Reset Day
        </button>
      </div>
      
      {/* Custom Amount */}
      <div className="mb-6">
        <div className="flex items-center gap-2">
          <input 
            type="number" 
            className="flex-1 p-2 border border-blue-300 rounded-md" 
            placeholder="Custom amount (ml)"
            id="customAmount"
            min="1"
          />
          <button 
            className="bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600"
            onClick={() => {
              const input = document.getElementById('customAmount');
              const amount = parseInt(input.value);
              if (amount > 0) {
                addWater(amount);
                input.value = '';
              }
            }}
          >
            Add
          </button>
        </div>
      </div>
      
      {/* Today's Log */}
      {log.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-2">Today's Log</h3>
          <div className="bg-white rounded-md p-3 shadow-sm max-h-48 overflow-y-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-blue-700 border-b border-blue-100">
                  <th className="text-left py-1">Time</th>
                  <th className="text-right py-1">Amount</th>
                  <th className="text-right py-1">Total</th>
                </tr>
              </thead>
              <tbody>
                {log.map((entry, index) => (
                  <tr key={index} className="border-b border-blue-50">
                    <td className="py-1">{entry.time}</td>
                    <td className={`text-right py-1 ${entry.amount >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {entry.amount >= 0 ? '+' : ''}{entry.amount} ml
                    </td>
                    <td className="text-right py-1">{entry.total} ml</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      {/* History Section */}
      {history.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-blue-800 mb-2">Previous Days</h3>
          <div className="bg-white rounded-md p-3 shadow-sm max-h-48 overflow-y-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-blue-700 border-b border-blue-100">
                  <th className="text-left py-1">Date</th>
                  <th className="text-right py-1">Intake</th>
                  <th className="text-right py-1">Goal</th>
                  <th className="text-right py-1">%</th>
                </tr>
              </thead>
              <tbody>
                {history.slice().reverse().map((day, index) => {
                  const percent = Math.round((day.intake / day.goal) * 100);
                  return (
                    <tr key={index} className="border-b border-blue-50">
                      <td className="py-1">{day.date}</td>
                      <td className="text-right py-1">{day.intake} ml</td>
                      <td className="text-right py-1">{day.goal} ml</td>
                      <td className={`text-right py-1 ${percent >= 100 ? 'text-green-600 font-medium' : 'text-blue-600'}`}>
                        {percent}%
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}