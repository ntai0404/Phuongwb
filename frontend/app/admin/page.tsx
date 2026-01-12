'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/components/providers/auth-provider';
import { Play, Settings, Users, Database, X, Plus, Edit, Trash2, ArrowLeft } from 'lucide-react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import Link from 'next/link';

export default function AdminPage() {
  const { user } = useAuth();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [message, setMessage] = useState('');

  // Sources management state
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const [newSource, setNewSource] = useState({ name: '', url: '', category: '' });
  const [editingSource, setEditingSource] = useState<any>(null);

  // Users management state
  const [usersOpen, setUsersOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<any>(null);
  const [userDialogMessage, setUserDialogMessage] = useState('');

  const triggerCrawlMutation = useMutation({
    mutationFn: async () => {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/crawler/trigger`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({}), // Empty body for full crawl
      });
      if (!response.ok) {
        throw new Error('Failed to trigger crawl');
      }
      return response.json();
    },
    onSuccess: () => {
      setMessage('Crawl đã được kích hoạt thành công!');
      // Force refresh article list so category tabs reflect new crawl
      queryClient.invalidateQueries({ queryKey: ['articles'] });
    },
    onError: (error) => {
      setMessage('Lỗi: ' + error.message);
    },
  });

  // Sources queries and mutations
  const { data: sources, isLoading: sourcesLoading } = useQuery({
    queryKey: ['sources'],
    queryFn: async () => {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/sources`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) throw new Error('Failed to fetch sources');
      return response.json();
    },
    enabled: sourcesOpen,
  });

  const createSourceMutation = useMutation({
    mutationFn: async (sourceData: any) => {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/sources`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(sourceData),
      });
      if (!response.ok) throw new Error('Failed to create source');
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] });
      setNewSource({ name: '', url: '', category: '' });
      setMessage('Nguồn đã được tạo thành công!');
    },
    onError: (error) => {
      setMessage('Lỗi: ' + error.message);
    },
  });

  const updateSourceMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: any }) => {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/sources/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error('Failed to update source');
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] });
      setEditingSource(null);
      setMessage('Nguồn đã được cập nhật thành công!');
    },
    onError: (error) => {
      setMessage('Lỗi: ' + error.message);
    },
  });

  const deleteSourceMutation = useMutation({
    mutationFn: async (id: number) => {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/sources/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) throw new Error('Failed to delete source');
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] });
      setMessage('Nguồn đã được xóa thành công!');
    },
    onError: (error) => {
      setMessage('Lỗi: ' + error.message);
    },
  });

  // Users queries and mutations
  const { data: users, isLoading: usersLoading } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/auth/users`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) throw new Error('Failed to fetch users');
      return response.json();
    },
    enabled: usersOpen,
  });

  const updateUserRoleMutation = useMutation({
    mutationFn: async ({ id, role }: { id: number; role: string }) => {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/auth/users/${id}/role`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ role }),
      });
      if (!response.ok) throw new Error('Failed to update user role');
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setEditingUser(null);
      setMessage('Quyền người dùng đã được cập nhật thành công!');
    },
    onError: (error) => {
      setMessage('Lỗi: ' + error.message);
    },
  });

  // Redirect if not admin
  if (!user || user.role !== 'admin') {
    router.push('/');
    return null;
  }

  const handleTriggerCrawl = () => {
    triggerCrawlMutation.mutate();
  };

  const handleCreateSource = () => {
    if (!newSource.name || !newSource.url || !newSource.category) {
      setMessage('Vui lòng điền đầy đủ thông tin!');
      return;
    }
    createSourceMutation.mutate(newSource);
  };

  const handleUpdateSource = () => {
    if (!editingSource) return;
    updateSourceMutation.mutate({
      id: editingSource.id,
      data: {
        name: editingSource.name,
        url: editingSource.url,
        category: editingSource.category,
        is_active: editingSource.is_active,
      },
    });
  };

  const handleDeleteSource = (id: number) => {
    if (confirm('Bạn có chắc muốn xóa nguồn này?')) {
      deleteSourceMutation.mutate(id);
    }
  };

  const handleUpdateUserRole = () => {
    if (!editingUser) return;
    setUserDialogMessage('');
    updateUserRoleMutation.mutate({
      id: editingUser.id,
      role: editingUser.role,
    });
  };


  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8 flex items-center gap-4">
          <Link href="/">
            <Button variant="outline" size="sm" className="shadow-md hover:shadow-lg transform transition-all duration-200 hover:scale-105">
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Bảng Điều Khiển</h1>
            <p className="text-gray-600">Quản lý hệ thống VDaily</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Crawler Control */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Play className="w-5 h-5" />
                Điều khiển trình thu thập
              </CardTitle>
              <CardDescription>
                Kích hoạt thu thập tin tức thủ công
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button
                onClick={handleTriggerCrawl}
                disabled={triggerCrawlMutation.isPending}
                className="w-full bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 text-white font-medium py-2 px-4 rounded-md shadow-sm transform transition-all duration-200 hover:scale-105"
              >
                {triggerCrawlMutation.isPending ? 'Đang kích hoạt...' : 'Kích hoạt thu thập'}
              </Button>
              {message && (
                <p className={`mt-2 text-sm ${message.includes('thành công') ? 'text-green-600' : 'text-red-600'}`}>
                  {message}
                </p>
              )}
            </CardContent>
          </Card>

          {/* Sources Management */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="w-5 h-5" />
                Nguồn tin
              </CardTitle>
              <CardDescription>
                Quản lý nguồn tin
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Dialog open={sourcesOpen} onOpenChange={setSourcesOpen}>
                <DialogTrigger asChild>
                  <Button className="w-full border border-gray-300 hover:bg-gray-50 transform transition-all duration-200 hover:scale-105">
                    Quản lý nguồn
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
                  <DialogHeader>
                    <DialogTitle>Quản lý nguồn tin</DialogTitle>
                    <DialogDescription>
                      Thêm, sửa, xóa các nguồn tin
                    </DialogDescription>
                  </DialogHeader>

                  {/* Add new source form */}
                  <div className="space-y-4 mb-6 p-4 border rounded-lg">
                    <h3 className="text-lg font-semibold">Thêm nguồn mới</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <Label htmlFor="source-name">Tên nguồn</Label>
                        <Input
                          id="source-name"
                          value={newSource.name}
                          onChange={(e) => setNewSource({ ...newSource, name: e.target.value })}
                          placeholder="Ví dụ: VNExpress"
                        />
                      </div>
                      <div>
                        <Label htmlFor="source-url">URL nguồn</Label>
                        <Input
                          id="source-url"
                          value={newSource.url}
                          onChange={(e) => setNewSource({ ...newSource, url: e.target.value })}
                          placeholder="https://vnexpress.net/rss/tin-moi-nhat.rss"
                        />
                      </div>
                      <div>
                        <Label htmlFor="source-category">Danh mục</Label>
                        <Input
                          id="source-category"
                          value={newSource.category}
                          onChange={(e) => setNewSource({ ...newSource, category: e.target.value })}
                          placeholder="Ví dụ: Tin tức"
                        />
                      </div>
                    </div>
                    <Button onClick={handleCreateSource} disabled={createSourceMutation.isPending}>
                      {createSourceMutation.isPending ? 'Đang tạo...' : 'Thêm nguồn'}
                    </Button>
                  </div>

                  {/* Sources table */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Danh sách nguồn</h3>
                    {sourcesLoading ? (
                      <p>Đang tải...</p>
                    ) : (
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Tên</TableHead>
                            <TableHead>URL</TableHead>
                            <TableHead>Danh mục</TableHead>
                            <TableHead>Trạng thái</TableHead>
                            <TableHead>Thao tác</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {sources?.map((source: any) => (
                            <TableRow key={source.id}>
                              <TableCell>{source.name}</TableCell>
                              <TableCell className="max-w-xs truncate">{source.url}</TableCell>
                              <TableCell>{source.category}</TableCell>
                              <TableCell>{source.is_active ? 'Hoạt động' : 'Tạm dừng'}</TableCell>
                              <TableCell>
                                <div className="flex gap-2">
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => setEditingSource(source)}
                                  >
                                    <Edit className="w-4 h-4" />
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => handleDeleteSource(source.id)}
                                  >
                                    <Trash2 className="w-4 h-4" />
                                  </Button>
                                </div>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    )}
                  </div>

                  {/* Edit source dialog */}
                  {editingSource && (
                    <Dialog open={!!editingSource} onOpenChange={() => setEditingSource(null)}>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Chỉnh sửa nguồn</DialogTitle>
                        </DialogHeader>
                        <div className="space-y-4">
                          <div>
                            <Label htmlFor="edit-name">Tên nguồn</Label>
                            <Input
                              id="edit-name"
                              value={editingSource.name}
                              onChange={(e) => setEditingSource({ ...editingSource, name: e.target.value })}
                            />
                          </div>
                          <div>
                            <Label htmlFor="edit-url">URL nguồn</Label>
                            <Input
                              id="edit-url"
                              value={editingSource.url}
                              onChange={(e) => setEditingSource({ ...editingSource, url: e.target.value })}
                            />
                          </div>
                          <div>
                            <Label htmlFor="edit-category">Danh mục</Label>
                            <Input
                              id="edit-category"
                              value={editingSource.category}
                              onChange={(e) => setEditingSource({ ...editingSource, category: e.target.value })}
                            />
                          </div>
                          <div className="flex items-center space-x-2">
                            <input
                              type="checkbox"
                              id="edit-active"
                              checked={editingSource.is_active}
                              onChange={(e) => setEditingSource({ ...editingSource, is_active: e.target.checked })}
                            />
                            <Label htmlFor="edit-active">Hoạt động</Label>
                          </div>
                          <div className="flex gap-2">
                            <Button onClick={handleUpdateSource} disabled={updateSourceMutation.isPending}>
                              {updateSourceMutation.isPending ? 'Đang cập nhật...' : 'Cập nhật'}
                            </Button>
                            <Button variant="outline" onClick={() => setEditingSource(null)}>
                              Hủy
                            </Button>
                          </div>
                        </div>
                      </DialogContent>
                    </Dialog>
                  )}
                </DialogContent>
              </Dialog>
            </CardContent>
          </Card>

          {/* User Management */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5" />
                Quản lý người dùng
              </CardTitle>
              <CardDescription>
                Quản lý người dùng và quyền
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Dialog open={usersOpen} onOpenChange={setUsersOpen}>
                <DialogTrigger asChild>
                  <Button className="w-full border border-gray-300 hover:bg-gray-50 transform transition-all duration-200 hover:scale-105">
                    Quản lý người dùng
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
                  <DialogHeader>
                    <DialogTitle>Quản lý người dùng</DialogTitle>
                    <DialogDescription>
                      Xem và thay đổi quyền của người dùng
                    </DialogDescription>
                  </DialogHeader>

                  {/* Users table */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Danh sách người dùng</h3>
                    {usersLoading ? (
                      <p>Đang tải...</p>
                    ) : (
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>ID</TableHead>
                            <TableHead>Tên đăng nhập</TableHead>
                            <TableHead>Email</TableHead>
                            <TableHead>Vai trò</TableHead>
                            <TableHead>Thao tác</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {users?.map((user: any) => (
                            <TableRow key={user.id}>
                              <TableCell>{user.id}</TableCell>
                              <TableCell>{user.username}</TableCell>
                              <TableCell>{user.email || 'N/A'}</TableCell>
                              <TableCell>{user.role}</TableCell>
                              <TableCell>
                                <div className="flex gap-2">
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => setEditingUser(user)}
                                  >
                                    <Edit className="w-4 h-4" />
                                  </Button>
                                  {/* Nút xóa người dùng đã bị loại bỏ */}
                                </div>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    )}
                  </div>

                  {/* Edit user dialog */}
                  {editingUser && (
                    <Dialog open={!!editingUser} onOpenChange={() => { setEditingUser(null); setUserDialogMessage(''); }}>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Thay đổi quyền hoặc xóa người dùng</DialogTitle>
                        </DialogHeader>
                        <div className="space-y-4">
                          <div>
                            <Label>Tên đăng nhập: {editingUser.username}</Label>
                          </div>
                          <div>
                            <Label htmlFor="user-role">Vai trò</Label>
                            <Select
                              value={editingUser.role}
                              onValueChange={(value) => setEditingUser({ ...editingUser, role: value })}
                            >
                              <SelectTrigger>
                                <SelectValue placeholder="Chọn vai trò" />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="user">User</SelectItem>
                                <SelectItem value="admin">Admin</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                          <div className="flex gap-2">
                            <Button onClick={handleUpdateUserRole} disabled={updateUserRoleMutation.isPending}>
                              {updateUserRoleMutation.isPending ? 'Đang cập nhật...' : 'Cập nhật'}
                            </Button>
                            <Button variant="outline" onClick={() => setEditingUser(null)}>
                              Hủy
                            </Button>
                            {/* Nút xóa người dùng đã bị loại bỏ */}
                          </div>
                          {userDialogMessage && (
                            <p className={`mt-2 text-sm ${userDialogMessage.includes('thành công') ? 'text-green-600' : 'text-red-600'}`}>
                              {userDialogMessage}
                            </p>
                          )}
                        </div>
                      </DialogContent>
                    </Dialog>
                  )}
                </DialogContent>
              </Dialog>
            </CardContent>
          </Card>
        </div>

        <div className="mt-8">
          <Card>
            <CardHeader>
              <CardTitle>Các Hành Động Nhanh</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <p className="text-sm text-gray-600">
                  • Kích hoạt thu thập: Kích hoạt thu thập tin tức từ tất cả nguồn
                </p>
                <p className="text-sm text-gray-600">
                  • Quản lý nguồn: Thêm/sửa/xóa nguồn tin
                </p>
                <p className="text-sm text-gray-600">
                  • Quản lý người dùng: Thay đổi quyền người dùng
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}