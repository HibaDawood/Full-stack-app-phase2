// components/LanguageSelector.tsx
import React from 'react';
import { useLanguage } from '@/contexts/LanguageContext';

const LanguageSelector: React.FC = () => {
  const { language, setLanguage, t } = useLanguage();

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLanguage(e.target.value as 'en' | 'zh');
  };

  return (
    <div className="flex items-center space-x-2">
      <label htmlFor="language-select" className="text-sm text-gray-700">
        {t('language')}:
      </label>
      <select
        id="language-select"
        value={language}
        onChange={handleLanguageChange}
        className="px-2 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="en">English</option>
        <option value="zh">中文</option>
      </select>
    </div>
  );
};

export default LanguageSelector;