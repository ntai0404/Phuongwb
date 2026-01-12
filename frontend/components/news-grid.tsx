"use client";

import { useState, useEffect } from 'react';
import { Article } from '@/lib/api';
import NewsCard from './news-card';
import NewsCardSkeleton from './news-card-skeleton';
import { AlertCircle, Loader2 } from 'lucide-react';
import { useInView } from 'react-intersection-observer';
import NewsDetailModal from './news-detail-modal';

interface NewsGridProps {
  articles: Article[];
  loading?: boolean;
  error?: string;
  fetchNextPage?: () => void;
  hasNextPage?: boolean;
  isFetchingNextPage?: boolean;
  showFeatured?: boolean;
}

export default function NewsGrid({
  articles,
  loading,
  error,
  fetchNextPage,
  hasNextPage,
  isFetchingNextPage,
  showFeatured = true
}: NewsGridProps) {
  const { ref, inView } = useInView();
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);

  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage?.();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <NewsCardSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600" />
          <div>
            <h3 className="text-lg font-semibold text-red-900">Lỗi tải tin tức</h3>
            <p className="text-red-700 mt-1">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (articles.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📰</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Không có tin tức nào</h3>
        <p className="text-gray-600">Hãy thử tìm kiếm với từ khóa khác</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Featured first article - chỉ hiển thị khi showFeatured = true (tab Tất cả) */}
      {showFeatured && articles[0] && (
        <div>
          <NewsCard
            key={articles[0].id}
            article={articles[0]}
            variant="large"
          />
        </div>
      )}

      {/* Grid of remaining articles */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {(showFeatured ? articles.slice(1) : articles).map((article) => (
          <NewsCard
            key={article.id}
            article={article}
            variant="small"
          />
        ))}
      </div>

      {/* Detail Modal */}
      <NewsDetailModal
        article={selectedArticle}
        isOpen={!!selectedArticle}
        onClose={() => {
          setSelectedArticle(null);
        }}
        onArticleSelect={(article) => {
          setSelectedArticle(article);
        }}
      />

      {/* Infinite Scroll Trigger */}
      <div ref={ref} className="flex justify-center py-8">
        {isFetchingNextPage ? (
          <div className="flex items-center gap-2 text-gray-600">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Đang tải thêm...</span>
          </div>
        ) : hasNextPage ? (
          <div className="text-gray-500 text-sm">
            Cuộn xuống để xem thêm
          </div>
        ) : articles.length > 0 ? (
          <div className="text-gray-500 text-sm">
            Đã hết tin tức
          </div>
        ) : null}
      </div>
    </div>
  );
}
