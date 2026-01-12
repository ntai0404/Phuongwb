'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/providers/auth-provider';
import { useQuery } from '@tanstack/react-query';
import TopBar from '@/components/topbar';
import Sidebar from '@/components/sidebar';
import NewsGrid from '@/components/news-grid';
import { Article, articlesApi } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function HistoryPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const { data: historyArticles, isLoading, refetch } = useQuery({
    queryKey: ['reading-history', user?.id || 1],
    queryFn: async () => {
      return await articlesApi.getReadingHistory();
    },
    refetchOnWindowFocus: true,
    staleTime: 0, // Always refetch
  });

  const filteredArticles = historyArticles?.filter((article: Article) =>
    article.title.toLowerCase().includes(search.toLowerCase()) ||
    article.summary?.toLowerCase().includes(search.toLowerCase())
  ) || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <TopBar search={search} onSearchChange={setSearch} />

      <div className="flex">
        <Sidebar selectedCategory={selectedCategory} onCategoryChange={setSelectedCategory} />

        <main className="flex-1 p-6">
          <div className="max-w-7xl mx-auto">
            <div className="mb-6 flex items-center gap-4">
              <Link href="/">
                <Button variant="outline" size="sm" className="shadow-md hover:shadow-lg transform transition-all duration-200 hover:scale-105">
                  <ArrowLeft className="w-4 h-4" />
                </Button>
              </Link>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Lịch sử đọc</h1>
                <p className="text-gray-600">Danh sách các bài viết bạn đã đọc</p>
              </div>
            </div>

            {isLoading ? (
              <div className="text-center py-12">
                <p className="text-gray-500">Đang tải...</p>
              </div>
            ) : filteredArticles.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-500">Bạn chưa đọc bài viết nào</p>
              </div>
            ) : (
              <NewsGrid articles={filteredArticles} showFeatured={false} />
            )}
          </div>
        </main>
      </div>
    </div>
  );
}