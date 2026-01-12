'use client';

import { useState } from 'react';
import { User, Bookmark, History } from 'lucide-react';
import { useAuth } from '@/components/providers/auth-provider';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface SidebarProps {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

export default function Sidebar({ selectedCategory, onCategoryChange }: SidebarProps) {
  const { user } = useAuth();
  const pathname = usePathname();

  // Determine if we're on a special page (saved/history) or home
  const isOnSpecialPage = pathname === '/saved' || pathname === '/history';
  const isOnHome = pathname === '/';

  const categories = [
    { id: 'all', name: 'Tất cả' },
    { id: 'business', name: 'Kinh doanh' },
    { id: 'technology', name: 'Công nghệ' },
    { id: 'sports', name: 'Thể thao' },
    { id: 'entertainment', name: 'Giải trí' },
    { id: 'politics', name: 'Chính trị' },
  ];

  const handleCategoryClick = (categoryId: string) => {
    if (isOnSpecialPage) {
      // Navigate to home with the selected category
      window.location.href = `/?category=${categoryId}`;
    } else {
      // Normal category change
      onCategoryChange(categoryId);
      // Scroll to top when changing category
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-6 sticky top-0 h-screen overflow-y-auto shadow-sm">
      {/* User Info */}
      {user && (
        <div className="mb-6 pb-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="font-medium text-gray-900 text-sm">{user.username}</p>
              <p className="text-xs text-gray-500 capitalize">{user.role}</p>
            </div>
          </div>
        </div>
      )}

      {/* User Actions */}
      {user && (
        <div className="mb-6 space-y-2">
          <Link href="/saved">
            <button className={`w-full flex items-center gap-3 px-4 py-3 text-left rounded-md transition-all duration-200 ${
              pathname === '/saved'
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-600 font-medium'
                : 'text-gray-700 hover:bg-gray-50'
            }`}>
              <Bookmark className="w-4 h-4" />
              <span className="text-sm">Đã lưu</span>
            </button>
          </Link>
          <Link href="/history">
            <button className={`w-full flex items-center gap-3 px-4 py-3 text-left rounded-md transition-all duration-200 ${
              pathname === '/history'
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-600 font-medium'
                : 'text-gray-700 hover:bg-gray-50'
            }`}>
              <History className="w-4 h-4" />
              <span className="text-sm">Lịch sử</span>
            </button>
          </Link>
        </div>
      )}

      {/* Categories */}
      <nav className="space-y-1">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Danh mục</h3>
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => handleCategoryClick(category.id)}
            className={`w-full text-left px-4 py-3 rounded-md transition-all duration-200 ${
              isOnHome && selectedCategory === category.id
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-600 font-medium'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            }`}
          >
            <span className="capitalize text-sm">{category.name}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}
