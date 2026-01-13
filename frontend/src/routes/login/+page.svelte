<script lang="ts">
  import { api } from "$lib/api/client";
  import { auth, saveToken } from "$lib/stores/auth";
  import { goto } from "$app/navigation";

  let email = "";
  let password = "";
  let error = "";
  let loading = false;

  async function submit() {
    error = "";
    loading = true;
    try {
      const res = await api<{ access_token: string }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });

      saveToken(res.access_token);

      const me = await api<any>("/me");
      const feats = await api<{ features: string[] }>("/me/features");

      auth.update((s) => ({
        ...s,
        me,
        features: new Set(feats.features),
        ready: true
      }));

      goto("/scheduler");
    } catch (e: any) {
      error = e?.message ?? "Error de login";
    } finally {
      loading = false;
    }
  }
</script>

<h1>Login</h1>

<form on:submit|preventDefault={submit} style="display:grid; gap:10px; max-width:340px;">
  <input placeholder="Email" bind:value={email} />
  <input placeholder="Password" type="password" bind:value={password} />
  <button type="submit" disabled={loading}>
    {loading ? "Entrando..." : "Entrar"}
  </button>
</form>

{#if error}
  <p style="color:red; margin-top:10px;">{error}</p>
{/if}
