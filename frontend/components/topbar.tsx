'use client';

import { Search, LogIn, LogOut, User, BookOpen, Bookmark, History } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { useAuth } from '@/components/providers/auth-provider';
import Link from 'next/link';

interface TopBarProps {
  search: string;
  onSearchChange: (search: string) => void;
}

export default function TopBar({
  search,
  onSearchChange,
}: TopBarProps) {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 sticky top-0 z-10 shadow-sm">
      <div className="w-full max-w-7xl mx-auto flex items-center justify-between">
        {/* Left - Logo */}
        <div className="flex items-center gap-3">
          <BookOpen className="w-8 h-8 text-blue-600" />
          <div className="text-2xl font-bold text-gray-900">
            VDaily
          </div>
        </div>

        {/* Center - Search */}
        <div className="flex-1 max-w-md mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              type="text"
              placeholder="Tìm kiếm tin tức..."
              value={search}
              onChange={(e) => onSearchChange(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 bg-white placeholder:text-gray-500 focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-0 text-sm transition-all duration-200 hover:border-gray-400 focus:border-blue-500 rounded-md"
            />
          </div>
        </div>

        {/* Right - Auth buttons */}
        <div className="flex items-center gap-4">
          {user ? (
            <div className="flex items-center gap-3">
              {user.role === 'admin' && (
                <Link href="/admin">
                  <Button variant="outline" size="sm" className="text-xs border border-gray-300 hover:bg-gray-50 transform transition-all duration-200 hover:scale-105 shadow-md hover:shadow-lg">
                    Quản trị viên
                  </Button>
                </Link>
              )}
              <Button
                variant="outline"
                size="sm"
                onClick={logout}
                className="flex items-center gap-1 border border-gray-300 hover:bg-gray-50 transform transition-all duration-200 hover:scale-105 shadow-md hover:shadow-lg"
              >
                <LogOut className="w-3 h-3" />
                Đăng xuất
              </Button>
            </div>
          ) : (
            <Link href="/auth">
              <Button 
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-md shadow-sm transform transition-all duration-200 hover:scale-105 shadow-md hover:shadow-lg"
              >
                <User className="w-4 h-4 mr-2" />
                Đăng nhập
              </Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
