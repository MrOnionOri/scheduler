import { PUBLIC_API_BASE } from "$env/static/public";
import { auth } from "$lib/stores/auth";
import { get } from "svelte/store";

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = get(auth).token;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string> | undefined)
  };

  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${PUBLIC_API_BASE}${path}`, { ...init, headers });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`${res.status} ${res.statusText}${text ? " - " + text : ""}`);
  }

  return res.json() as Promise<T>;
}
