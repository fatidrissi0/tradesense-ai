export interface User {
  id: number;
  username: string;
  email: string;
  role: 'user' | 'admin' | 'superadmin';
  created_at: string;
  is_active: boolean;
}
