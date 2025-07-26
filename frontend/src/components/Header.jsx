import React from 'react';
import { useTranslation } from 'react-i18next';

export default function Header() {
  const { i18n, t } = useTranslation();
  return (
    <header className="bg-white shadow p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold text-primary">{t('AI Video Studio')}</h1>
      <select
        value={i18n.language}
        onChange={e => i18n.changeLanguage(e.target.value)}
        className="border rounded p-1"
      >
        <option value="en">EN</option>
        <option value="es">ES</option>
      </select>
    </header>
  );
}
