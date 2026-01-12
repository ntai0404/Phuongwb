import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  rssSourcesApi,
  RSSSource,
  RSSSourceCreate,
  RSSSourceUpdate,
} from "@/lib/api";

export function useRSSSources() {
  return useQuery<RSSSource[], Error>({
    queryKey: ["rss-sources"],
    queryFn: rssSourcesApi.getAll,
  });
}

export function useCreateRSSSource() {
  const queryClient = useQueryClient();

  return useMutation<RSSSource, Error, RSSSourceCreate>({
    mutationFn: rssSourcesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["rss-sources"] });
    },
  });
}

export function useUpdateRSSSource() {
  const queryClient = useQueryClient();

  return useMutation<RSSSource, Error, { id: number; data: RSSSourceUpdate }>({
    mutationFn: ({ id, data }) => rssSourcesApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["rss-sources"] });
    },
  });
}

export function useDeleteRSSSource() {
  const queryClient = useQueryClient();

  return useMutation<void, Error, number>({
    mutationFn: rssSourcesApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["rss-sources"] });
    },
  });
}
