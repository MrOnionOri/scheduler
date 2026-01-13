<script lang="ts">
  import { onMount } from "svelte";
  import { auth, loadTokenFromStorage, logout } from "$lib/stores/auth";
  import { api } from "$lib/api/client";
  import { goto } from "$app/navigation";
  import "../app.css";

  let isBeta = false;

  onMount(async () => {
    // Carga token guardado
    loadTokenFromStorage();

    try {
      // si hay token, intentamos cargar usuario + features
      const me = await api<any>("/me");
      const feats = await api<{ features: string[] }>("/me/features");

      auth.update((s) => ({
        ...s,
        me,
        features: new Set(feats.features),
        ready: true
      }));
    } catch {
      // no auth o token inválido
      auth.update((s) => ({ ...s, me: null, features: new Set(), ready: true }));
    }
  });

  function doLogout() {
    logout();
    goto("/login");
  }

  $: isBeta = $auth.features?.has("beta_menu") ?? false;
</script>

<svelte:head>
  <!-- Si este archivo existe en /static/vendor/fullcalendar/ -->
</svelte:head>

<nav style="display:flex; gap:12px; padding:12px; border-bottom:1px solid #ddd;">
  <a href="/" style="font-weight:700;">Scheduler</a>
  <a href="/scheduler">Agenda</a>

  {#if isBeta}
    <a href="/beta">Beta</a>
  {/if}

  <div style="margin-left:auto;">
    {#if $auth.me}
      <span style="margin-right:10px;">{$auth.me.email}</span>
      <button on:click={doLogout}>Salir</button>
    {:else}
      <a href="/login">Login</a>
    {/if}
  </div>
</nav>

<main style="padding:16px;">
  <slot />
</main>
