'use client';

import { Article } from '@/lib/api';
import { Calendar, Globe, Tag, X, ExternalLink, Bookmark, History } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useRelatedArticles } from '@/hooks/use-articles';
import { Button } from './ui/button';
import { useAuth } from './providers/auth-provider';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

interface NewsDetailModalProps {
    article: Article | null;
    isOpen: boolean;
    onClose: () => void;
    onArticleSelect?: (article: Article) => void;
}

export default function NewsDetailModal({ article, isOpen, onClose, onArticleSelect }: NewsDetailModalProps) {
    const { data: relatedArticles, isLoading: isLoadingRelated } = useRelatedArticles(article?.id || 0);
    const { user } = useAuth();
    const [isSaved, setIsSaved] = useState(false);
    const queryClient = useQueryClient();

    // Check if article is saved - use specific endpoint
    const { data: savedStatus } = useQuery({
        queryKey: ['saved-status', article?.id, user?.id],
        queryFn: async () => {
            if (!article?.id || !user?.id) return false;
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/articles/saved/${article.id}?user_id=${user.id}`);
            if (!response.ok) return false;
            const result = await response.json();
            return result.is_saved;
        },
        enabled: !!article && isOpen && !!user,
        staleTime: 30 * 1000, // 30 seconds
    });

    // Update isSaved state when savedStatus changes or article changes
    useEffect(() => {
        if (savedStatus !== undefined) {
            setIsSaved(savedStatus);
        }
    }, [savedStatus]);

    // Reset isSaved when article changes
    useEffect(() => {
        if (article?.id) {
            setIsSaved(false); // Reset and wait for query to update
        }
    }, [article?.id]);

    // Save/unsave article mutation
    const saveArticleMutation = useMutation({
        mutationFn: async (articleId: number) => {
            if (!user?.id) throw new Error('User not authenticated');
            const method = isSaved ? 'DELETE' : 'POST';
            console.log('Save mutation called:', { articleId, method, isSaved });
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/articles/save/${articleId}?user_id=${user.id}`, {
                method,
            });
            console.log('Save API response:', response.status, await response.text());
            if (!response.ok) throw new Error('Failed to save/unsave article');
            return { success: true, wasSaved: isSaved };
        },
        onSuccess: (result) => {
            console.log('Save mutation success:', result);
            // Update local state
            setIsSaved(!result.wasSaved);
            // Invalidate saved articles queries
            queryClient.invalidateQueries({ queryKey: ['saved-articles'] });
            queryClient.invalidateQueries({ queryKey: ['saved-status'] });
        },
        onError: (error) => {
            console.error('Save mutation error:', error);
        },
    });

    // Mark as read when modal opens - only once per article
    const markAsReadMutation = useMutation({
        mutationFn: async (articleId: number) => {
            if (!user?.id) throw new Error('User not authenticated');
            console.log('Mark as read called:', { articleId });
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/articles/read/${articleId}?user_id=${user.id}`, {
                method: 'POST',
            });
            console.log('Mark as read response:', response.status, await response.text());
            if (!response.ok) throw new Error('Failed to mark as read');
            return response.json();
        },
        onSuccess: () => {
            console.log('Mark as read success');
            // Invalidate reading history queries
            queryClient.invalidateQueries({ queryKey: ['reading-history'] });
        },
        onError: (error) => {
            console.error('Mark as read error:', error);
        },
    });

    // Track which articles have been marked as read in this session
    const [markedAsRead, setMarkedAsRead] = useState<Set<number>>(new Set());

    useEffect(() => {
        // Mark article as read when modal opens for the first time
        if (isOpen && article?.id && !markedAsRead.has(article.id)) {
            markAsReadMutation.mutate(article.id);
            setMarkedAsRead(prev => new Set(prev).add(article.id));
        }
    }, [isOpen, article?.id, markedAsRead, markAsReadMutation]);

    useEffect(() => {
        // Reset modal state when closing
        if (!isOpen) {
            setIsSaved(false);
        }
    }, [isOpen]);

    useEffect(() => {
        // Allow scrolling when modal is open
        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }

        return () => {
            document.body.style.overflow = 'unset';
        };
    }, [isOpen]);

    const handleSaveArticle = () => {
        if (article?.id) {
            saveArticleMutation.mutate(article.id);
        }
    };

    if (!isOpen || !article) return null;

    return (
        <div className="fixed inset-0 z-50 bg-black/60 transition-all duration-300">
            <div
                className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-50 w-full max-w-5xl max-h-[90vh] border border-gray-200 flex flex-col overflow-hidden shadow-lg rounded-lg"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Header */}
                <div className="border-b border-gray-200 p-4 flex justify-between items-center bg-white rounded-t-lg">
                    <div className="text-xl font-bold text-gray-900">Chi tiết bài viết</div>
                    <div className="flex items-center gap-2">
                        {user && (
                            <Button
                                onClick={handleSaveArticle}
                                disabled={saveArticleMutation.isPending}
                                variant="outline"
                                size="sm"
                                className={`flex items-center gap-2 ${isSaved ? 'bg-blue-50 border-blue-200 text-blue-700' : ''}`}
                            >
                                <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-current' : ''}`} />
                                {saveArticleMutation.isPending ? 'Đang xử lý...' : isSaved ? 'Đã lưu' : 'Lưu'}
                            </Button>
                        )}
                        <button
                            onClick={onClose}
                            className="p-2 hover:bg-gray-100 transition-colors rounded"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-6 md:p-8 bg-gray-50 font-sans text-gray-900">
                    <div className="max-w-3xl mx-auto">
                        {/* Article Header */}
                        <header className="mb-8 text-center">
                            <div className="flex justify-center items-center gap-4 mb-4 text-sm text-gray-500">
                                <span>{article.source?.name || 'Nguồn'}</span>
                                <span>•</span>
                                <span>{article.published || 'Hôm nay'}</span>
                                <span>•</span>
                                <span>{article.source?.category || article.category || 'Tin tức'}</span>
                            </div>

                            <h1 className="text-3xl md:text-4xl font-bold leading-tight mb-4 text-gray-900">
                                {article.title}
                            </h1>

                            <div className="text-lg italic text-gray-700 max-w-2xl mx-auto first-letter:text-2xl first-letter:font-bold first-letter:uppercase">
                                {article.summary}
                            </div>
                        </header>

                        {/* Feature Image */}
                        {article.image_url && (
                            <div className="mb-8 border border-gray-200 p-2 bg-white rounded">
                                {/* eslint-disable-next-line @next/next/no-img-element */}
                                <img
                                    src={article.image_url}
                                    alt={article.title}
                                    className="w-full h-auto rounded"
                                />
                            </div>
                        )}

                        {/* Article Body */}
                        <div
                            className="prose prose-lg max-w-none text-gray-900 leading-relaxed"
                            dangerouslySetInnerHTML={{ __html: article.content || '<p className="italic text-gray-500">Nội dung đầy đủ chưa có.</p>' }}
                        />

                        {/* Footer Links */}
                        <footer className="mt-12 pt-6 border-t border-gray-200 flex justify-center">
                            <a
                                href={article.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 px-4 py-2 bg-black text-white font-semibold hover:bg-gray-800 transition-colors"
                            >
                                Xem nguồn gốc
                                <ExternalLink className="w-4 h-4" />
                            </a>
                        </footer>

                        {/* Related Articles */}
                        <section className="mt-12 pt-6 border-t border-gray-200">
                            <h3 className="text-xl font-bold mb-6 text-center">Bài viết liên quan</h3>

                            {isLoadingRelated ? (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    {[1, 2, 3, 4].map((i) => (
                                        <div key={i} className="h-20 bg-gray-100 animate-pulse rounded" />
                                    ))}
                                </div>
                            ) : relatedArticles && relatedArticles.length > 0 ? (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    {relatedArticles.map((rel) => (
                                        <div
                                            key={rel.id}
                                            className="bg-white p-4 hover:bg-gray-50 transition-colors cursor-pointer border border-gray-200 rounded"
                                            onClick={() => onArticleSelect?.(rel)}
                                        >
                                            <div className="text-xs text-blue-600 mb-1">{rel.source?.name}</div>
                                            <h4 className="text-sm font-semibold leading-tight text-gray-900">{rel.title}</h4>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="text-center py-6 text-gray-500">
                                    Không có bài viết liên quan.
                                </div>
                            )}
                        </section>
                    </div>
                </div>
            </div>

            {/* Click outside to close */}
            <div className="fixed inset-0 -z-10" onClick={onClose} />
        </div>
    );
}
