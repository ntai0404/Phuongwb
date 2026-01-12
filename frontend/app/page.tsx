'use client';

import { useMemo, useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import TopBar from "@/components/topbar";
import Sidebar from "@/components/sidebar";
import NewsGrid from "@/components/news-grid";
import { useArticles } from "@/hooks/use-articles";

function HomeContent() {
  const searchParams = useSearchParams();
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [search, setSearch] = useState("");

  // Read category from URL params
  useEffect(() => {
    const categoryParam = searchParams.get('category');
    if (categoryParam) {
      setSelectedCategory(categoryParam);
    }
  }, [searchParams]);

  // Use React Query to fetch articles
  const {
    data,
    isLoading,
    error,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage
  } = useArticles();

  const news = useMemo(() => {
    return data?.pages.flat() || [];
  }, [data]);

  // Helper to normalize category names
  const normalizeCategoryName = (cat: string | undefined) => {
    if (!cat) return "Khác";
    const categoryMap: Record<string, string> = {
      "business": "Kinh doanh",
      "technology": "Công nghệ",
      "sports": "Thể thao",
      "entertainment": "Giải trí",
      "politics": "Chính trị",
      "health": "Sức khỏe",
      "education": "Giáo dục",
      "law": "Pháp luật",
      // If already in Vietnamese, return as is
      "Kinh doanh": "Kinh doanh",
      "Công nghệ": "Công nghệ",
      "Thể thao": "Thể thao",
      "Giải trí": "Giải trí",
      "Chính trị": "Chính trị",
    };
    return categoryMap[cat.toLowerCase()] || cat;
  };

  // Get Vietnamese category name for display
  const getCategoryDisplayName = (categoryId: string) => {
    const categoryMap: Record<string, string> = {
      "all": "Tin tức mới nhất",
      "business": "Kinh doanh",
      "technology": "Công nghệ",
      "sports": "Thể thao",
      "entertainment": "Giải trí",
      "politics": "Chính trị",
    };
    return categoryMap[categoryId] || categoryId;
  };

  const filteredNews = useMemo(() => {
    return news.filter((item) => {
      const category = normalizeCategoryName(item.category || item.source?.category);
      const categoryMap = {
        all: true,
        business: category === "Kinh doanh",
        technology: category === "Công nghệ",
        sports: category === "Thể thao",
        entertainment: category === "Giải trí",
        politics: category === "Chính trị",
      };
      const matchCategory = categoryMap[selectedCategory as keyof typeof categoryMap] ?? true;

      const kw = search.trim().toLowerCase();
      const matchSearch =
        !kw ||
        item.title?.toLowerCase().includes(kw) ||
        item.summary?.toLowerCase().includes(kw) ||
        item.source?.name?.toLowerCase().includes(kw);

      return matchCategory && matchSearch;
    });
  }, [news, selectedCategory, search]);

  return (
    <div className="min-h-screen bg-gray-50 font-sans flex">
      {/* Sidebar */}
      <Sidebar selectedCategory={selectedCategory} onCategoryChange={setSelectedCategory} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <TopBar
          search={search}
          onSearchChange={setSearch}
        />

        {/* Main Content Area */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1">
          {/* Content Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {getCategoryDisplayName(selectedCategory)}
            </h1>
            <p className="text-gray-600">
              {new Date().toLocaleDateString('vi-VN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </p>
          </div>

          {/* News Grid */}
          <NewsGrid
            articles={filteredNews}
            loading={isLoading}
            error={error?.message}
            fetchNextPage={fetchNextPage}
            hasNextPage={hasNextPage}
            isFetchingNextPage={isFetchingNextPage}
            showFeatured={selectedCategory === 'all'}
          />
        </main>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HomeContent />
    </Suspense>
  );
}
