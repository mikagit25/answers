'use client';

import React from 'react';

interface Tradition {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
}

interface TraditionSelectorProps {
  traditions: Tradition[];
  selectedTradition: string | null;
  onSelect: (traditionId: string) => void;
}

const TraditionSelector: React.FC<TraditionSelectorProps> = ({
  traditions,
  selectedTradition,
  onSelect,
}) => {
  return (
    <div className="w-full">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200">
        Выберите традицию
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {traditions.map((tradition) => (
          <button
            key={tradition.id}
            onClick={() => onSelect(tradition.id)}
            className={`
              p-4 rounded-xl border-2 transition-all duration-200
              flex flex-col items-center gap-2
              ${selectedTradition === tradition.id
                ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20 shadow-md'
                : 'border-gray-200 dark:border-gray-700 hover:border-primary-400 hover:shadow-sm'
              }
            `}
            aria-pressed={selectedTradition === tradition.id}
          >
            <span className="text-3xl" role="img" aria-label={tradition.name}>
              {tradition.icon}
            </span>
            <span className="text-sm font-medium text-center text-gray-800 dark:text-gray-200">
              {tradition.name}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default TraditionSelector;
