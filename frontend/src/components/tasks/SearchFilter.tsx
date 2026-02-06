import React from 'react';
import { useLanguage } from '@/contexts/LanguageContext';

interface SearchFilterProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  filterStatus: 'all' | 'pending' | 'in-progress' | 'completed';
  setFilterStatus: (status: 'all' | 'pending' | 'in-progress' | 'completed') => void;
  resetFilters: () => void;
}

const SearchFilter: React.FC<SearchFilterProps> = ({
  searchQuery,
  setSearchQuery,
  filterStatus,
  setFilterStatus,
  resetFilters
}) => {
  const { t } = useLanguage();

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Search Input */}
        <div>
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
            {t('search')}
          </label>
          <input
            type="text"
            id="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t('searchPlaceholder')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Status Filter */}
        <div>
          <label htmlFor="status-filter" className="block text-sm font-medium text-gray-700 mb-1">
            {t('filterByStatus')}
          </label>
          <select
            id="status-filter"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value as 'all' | 'pending' | 'in-progress' | 'completed')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">{t('statusAll')}</option>
            <option value="pending">{t('statusPending')}</option>
            <option value="in-progress">{t('statusInProgress')}</option>
            <option value="completed">{t('statusCompleted')}</option>
          </select>
        </div>

        {/* Reset Button */}
        <div className="flex items-end">
          <button
            onClick={resetFilters}
            className="w-full px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            {t('reset')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchFilter;