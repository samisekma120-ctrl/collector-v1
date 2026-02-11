export type UserRole = "buyer" | "seller" | "admin";

export type User = {
  id: string;
  email: string;
  role: UserRole;
  created_at: string;
};

export type Category = {
  id: string;
  name: string;
  created_at: string;
};

export type TokenResponse = {
  access_token: string;
  token_type?: string;
};
