<script lang="ts">
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";

  // si ya está logueado, mandarlo a scheduler
  $: if ($auth.ready && $auth.me) {
    goto("/scheduler");
  }
</script>

<h1>Scheduler</h1>

{#if !$auth.ready}
  <p>Cargando...</p>
{:else if !$auth.me}
  <p>Inicia sesión para ver tu agenda.</p>
  <a href="/login">Ir a Login</a>
{:else}
  <p>Redirigiendo...</p>
{/if}
