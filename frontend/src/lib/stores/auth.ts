import { writable } from "svelte/store";

export type Me = {
  id: number;
  email: string;
  full_name: string;
  roles: string[];
};

type AuthState = {
  token: string | null;
  me: Me | null;
  features: Set<string>;
  ready: boolean;
};

export const auth = writable<AuthState>({
  token: null,
  me: null,
  features: new Set(),
  ready: false
});

export function loadTokenFromStorage() {
  const token = localStorage.getItem("token");
  auth.update((s) => ({ ...s, token }));
}

export function saveToken(token: string | null) {
  if (token) localStorage.setItem("token", token);
  else localStorage.removeItem("token");
  auth.update((s) => ({ ...s, token }));
}

export function logout() {
  saveToken(null);
  auth.update((s) => ({
    ...s,
    me: null,
    features: new Set()
  }));
}
