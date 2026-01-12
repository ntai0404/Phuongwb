'use client';

import { useEffect, useState } from 'react';
import { articlesApi, Article } from '@/lib/api';
import TopBar from '@/components/topbar';
import Sidebar from '@/components/sidebar';
import NewsGrid from '@/components/news-grid';
import { ExternalLink, Bookmark, Share2, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface ArticlePageProps {
  params: Promise<{
    id: string;
  }>;
}

export default function ArticlePage({ params }: ArticlePageProps) {
  const router = useRouter();
  const [article, setArticle] = useState<Article | null>(null);
  const [relatedArticles, setRelatedArticles] = useState<Article[]>([]);
  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    router.push(`/?category=${category}`);
  };

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        setIsLoading(true);
        const { id } = await params;
        const data = await articlesApi.getById(Number(id));
        setArticle(data);
        
        // Check if article is saved
        const savedStatus = await articlesApi.checkSaved(Number(id));
        setIsSaved(savedStatus);
        
        // Mark as read
        await articlesApi.markAsRead(Number(id));

        // Fetch related articles using recommendation service with fallback
        const loadFallbackRelated = async () => {
          const allArticles = await articlesApi.getAll();
          return allArticles
            .filter((a: Article) => a.id !== data.id && a.source?.id === data.source?.id)
            .slice(0, 4);
        };

        try {
          const relatedIds = await articlesApi.getRecommendations(data.id, 4);
          if (relatedIds.length > 0) {
            const related = await articlesApi.getByIds(relatedIds);
            setRelatedArticles(related);
          } else {
            setRelatedArticles(await loadFallbackRelated());
          }
        } catch (err) {
          console.error('Failed to get recommendations:', err);
          setRelatedArticles(await loadFallbackRelated());
        }
      } catch (err) {
        setError('Không thể tải bài viết. Vui lòng thử lại sau.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchArticle();
  }, [params]);

  const handleSave = async () => {
    if (!article) return;
    try {
      if (isSaved) {
        await articlesApi.unsaveArticle(article.id);
      } else {
        await articlesApi.saveArticle(article.id);
      }
      setIsSaved(!isSaved);
    } catch (err) {
      console.error('Error saving article:', err);
    }
  };

  const handleShare = () => {
    if (!article) return;
    if (navigator.share) {
      navigator.share({
        title: article.title,
        text: article.summary,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('Đã sao chép liên kết!');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 font-sans flex">
        <Sidebar selectedCategory={selectedCategory} onCategoryChange={handleCategoryChange} />
        <div className="flex-1 flex flex-col">
          <TopBar search={''} onSearchChange={() => {}} />
          <div className="flex-1 flex items-center justify-center">
            <p className="text-gray-600">Đang tải bài viết...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="min-h-screen bg-gray-50 font-sans flex">
        <Sidebar selectedCategory={selectedCategory} onCategoryChange={handleCategoryChange} />
        <div className="flex-1 flex flex-col">
          <TopBar search={''} onSearchChange={() => {}} />
          <div className="flex-1 flex items-center justify-center p-12">
            <div className="max-w-md text-center">
              <h2 className="text-2xl font-bold mb-2">Không tìm thấy bài viết</h2>
              <p className="text-gray-600 mb-6">{error || 'Bài viết có thể đã bị xóa hoặc không tồn tại.'}</p>
              <button
                onClick={() => router.back()}
                className="inline-flex items-center gap-2 px-4 py-2 bg-black text-white font-semibold hover:bg-gray-900"
              >
                <ArrowLeft className="w-4 h-4" />
                Quay lại
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 font-sans flex">
      <Sidebar selectedCategory={selectedCategory} onCategoryChange={handleCategoryChange} />
      <div className="flex-1 flex flex-col">
        <TopBar search={''} onSearchChange={() => {}} />
        <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
          {/* Header with back button */}
          <button
            onClick={() => router.back()}
            className="flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium mb-6"
          >
            <ArrowLeft className="w-4 h-4" />
            Quay lại
          </button>

          {/* Article Metadata */}
          <div className="mb-4 text-sm font-semibold text-gray-600 uppercase tracking-wide">
            {article.source?.name} • {article.published ? new Date(article.published).toLocaleDateString('vi-VN') : 'Hôm nay'}
          </div>

          {/* Article Title */}
          <h1 className="text-4xl lg:text-5xl font-extrabold mb-6 leading-tight text-gray-900">
            {article.title}
          </h1>

          {/* Summary Section - Highlighted Box */}
          <div className="bg-blue-50 border-l-4 border-blue-500 p-6 mb-8 rounded">
            <h2 className="text-sm font-semibold text-gray-600 uppercase mb-2 tracking-wide">Tóm tắt</h2>
            <p className="text-lg font-medium text-gray-800 leading-relaxed">
              {article.summary}
            </p>
          </div>

          {/* Featured Image */}
          {article.image_url && (
            <div className="mb-8 bg-white border border-gray-200 p-1 rounded-lg overflow-hidden">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={article.image_url}
                alt={article.title}
                className="w-full h-auto object-cover"
              />
            </div>
          )}

          {/* Full Content Section */}
          <article className="prose prose-lg max-w-none mb-12 text-gray-800">
            <h2 className="text-2xl font-bold mb-6 mt-8">Chi tiết bài viết</h2>
            <div className="text-base leading-relaxed space-y-4">
              {article.content ? (
                <div dangerouslySetInnerHTML={{ __html: article.content }} />
              ) : (
                <p className="text-gray-500 italic">
                  Nội dung đầy đủ không có sẵn. Vui lòng truy cập nguồn gốc để đọc toàn bộ bài viết.
                </p>
              )}
            </div>
          </article>

          {/* Source Link Section */}
          <div className="bg-gray-100 p-6 rounded-lg mb-12 border border-gray-200">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">Nguồn gốc</h3>
            <p className="text-gray-600 mb-4">
              Đọc bài viết đầy đủ trên trang web gốc:
            </p>
            <a
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 bg-black text-white font-semibold hover:bg-gray-900 transition-colors rounded"
            >
              Đọc bài viết gốc
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-3 mb-12 pb-8 border-b border-gray-200">
            <button
              onClick={handleSave}
              className={`flex items-center gap-2 px-4 py-2 font-semibold rounded transition-colors ${
                isSaved
                  ? 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              <Bookmark className="w-4 h-4" />
              {isSaved ? 'Đã lưu' : 'Lưu bài viết'}
            </button>
            <button
              onClick={handleShare}
              className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 font-semibold hover:bg-gray-300 rounded transition-colors"
            >
              <Share2 className="w-4 h-4" />
              Chia sẻ
            </button>
          </div>

          {/* Related Articles Section */}
          {relatedArticles.length > 0 && (
            <div>
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Đọc thêm</h2>
              <NewsGrid articles={relatedArticles} />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
