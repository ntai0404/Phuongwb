import { useQuery, useInfiniteQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { articlesApi, Article } from '@/lib/api';

export function useArticles() {
  return useInfiniteQuery<Article[], Error>({
    queryKey: ['articles'],
    queryFn: ({ pageParam = 1 }) => articlesApi.getAll(pageParam as number, 20),
    initialPageParam: 1,
    getNextPageParam: (lastPage, allPages) => {
      // The backend returns 20 items per page regardless of limit.
      // If we get at least 20 items, there's likely another page.
      return lastPage.length >= 20 ? allPages.length + 1 : undefined;
    },
  });
}

export function useArticle(id: number) {
  return useQuery<Article, Error>({
    queryKey: ['article', id],
    queryFn: () => articlesApi.getById(id),
    enabled: !!id,
  });
}

export function useCreateArticle() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: articlesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] });
    },
  });
}

export function useUpdateArticle() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, article }: { id: number; article: Partial<Article> }) =>
      articlesApi.update(id, article),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['articles'] });
      queryClient.invalidateQueries({ queryKey: ['article', id] });
    },
  });
}

export function useDeleteArticle() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: articlesApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] });
    },
  });
}

export function useRelatedArticles(id: number) {
  return useQuery<Article[], Error>({
    queryKey: ['article', id, 'related'],
    queryFn: async () => {
      const ids = await articlesApi.getRecommendations(id);
      if (ids.length === 0) return [];
      return articlesApi.getByIds(ids);
    },
    enabled: !!id,
  });
}
