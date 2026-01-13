<script lang="ts">
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import { auth } from "$lib/stores/auth";
  import { api } from "$lib/api/client";
  import { goto } from "$app/navigation";

  import IPhoneCalendar from "$lib/components/IPhoneCalendar.svelte";
  import type { CalEvent } from "$lib/calendar/types";

  let events: CalEvent[] = [];
  let anchor = new Date();

  async function waitAuthReady() {
    while (!get(auth).ready) await new Promise(r => setTimeout(r, 50));
  }

  async function loadWeekEvents() {
    // por ahora: trae una ventana grande, luego refinamos con from/to por vista
    const from = new Date(anchor); from.setDate(from.getDate() - 14);
    const to = new Date(anchor); to.setDate(to.getDate() + 21);

    const params = new URLSearchParams();
    params.set("from_iso", from.toISOString());
    params.set("to_iso", to.toISOString());
    params.set("mine", "true");

    const acts = await api<any[]>(`/activities?${params.toString()}`);

    events = acts.map(a => ({
      id: a.id,
      title: a.title,
      start: a.start_at,
      end: a.end_at,
      approval_status: a.approval_status
    }));
  }

  function onCreateRange({ start, end }: { start: Date; end: Date }) {
    // aquí abrimos tu modal (o creamos directo)
    const title = prompt("Título de la actividad:");
    if (!title) return;

    api("/activities", {
      method: "POST",
      body: JSON.stringify({
        project_id: 1,              // luego lo conectamos a selector proyecto
        team_id: null,
        category_id: null,
        title,
        description: "",
        start_at: start.toISOString(),
        end_at: end.toISOString(),
        priority: "MEDIUM",
        kind: "PERSONAL_EXTRA",
        assignee_user_ids: []
      })
    }).then(loadWeekEvents);
  }

  function onEventClick(ev: CalEvent) {
    alert(ev.title);
  }

  onMount(async () => {
    await waitAuthReady();
    if (!get(auth).me) { goto("/login"); return; }
    await loadWeekEvents();
  });
</script>

<h1>Scheduler</h1>

<IPhoneCalendar
  {events}
  bind:anchor
  mode="week"
  onCreate={onCreateRange}
  onEventClick={onEventClick}
/>
