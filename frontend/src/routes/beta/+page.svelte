<script lang="ts">
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";

  $: if ($auth.ready) {
    const ok = $auth.features.has("beta_menu");
    if (!ok) goto("/scheduler");
  }
</script>

<h1>Beta Zone</h1>
<p>Esta sección solo aparece para usuarios con BETA_TESTER (o feature habilitado).</p>
