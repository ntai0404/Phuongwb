'use client';

import { Bookmark } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Article } from '@/lib/api';
import Link from 'next/link';

interface NewsCardProps {
  article: Article;
  variant?: 'small' | 'large';
}

export default function NewsCard({ article, variant = 'small' }: NewsCardProps) {
  const sourceName = article.source?.name || 'Nguồn';
  const category = article.source?.category || article.category || 'Khác';

  const isLarge = variant === 'large';

  return (
    <Link href={`/articles/${article.id}`}>
      <Card 
        className={`cursor-pointer transition-all duration-200 border border-gray-200 bg-white ${isLarge ? 'hover:shadow-2xl' : 'hover:shadow-lg hover:border-gray-300'}`}
      >
        <CardContent className="p-0">
          {article.image_url && (
            <div className={isLarge ? 'aspect-[16/7] relative overflow-hidden' : 'aspect-[16/9] relative overflow-hidden'}>
              <img
                src={article.image_url}
                alt={article.title}
                className={`w-full h-full object-cover transition-transform duration-200 ${isLarge ? '' : 'hover:scale-105'}`}
              />
            </div>
          )}

          <div className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded">
                {category}
              </span>
              <span className="text-xs text-gray-500">
                {article.published || 'Hôm nay'}
              </span>
            </div>

            <h3 className={`font-semibold text-gray-900 mb-2 leading-tight hover:text-blue-600 transition-colors ${isLarge ? 'text-3xl line-clamp-3' : 'text-lg line-clamp-2'}`}>
              {article.title}
            </h3>

            <p className={`text-sm text-gray-600 mb-3 leading-relaxed ${isLarge ? 'line-clamp-6' : 'line-clamp-4'}`}>
              {article.summary || 'Không có tóm tắt'}
            </p>

            <div className="flex items-center justify-between text-xs text-gray-500">
              <span className="font-medium">{sourceName}</span>
              <span className="hover:text-blue-600 transition-colors cursor-pointer">
                Đọc thêm →
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
