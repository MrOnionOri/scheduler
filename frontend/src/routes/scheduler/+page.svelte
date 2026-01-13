<script lang="ts">
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { api } from "$lib/api/client";
  import { goto } from "$app/navigation";
  import { get } from "svelte/store";

  import IPhoneCalendar from "$lib/components/IPhoneCalendar.svelte";
  import type { CalEvent } from "$lib/calendar/types";

  type Project = {
    id: number;
    name: string;
    description: string;
    is_active: boolean;
    owner_manager_id: number | null;
  };
  type Team = { id: number; project_id: number; name: string };

  type Activity = {
    id: number;
    project_id: number;
    team_id: number | null;
    category_id: number | null;
    title: string;
    description: string;
    start_at: string;
    end_at: string;
    priority: string;
    status: string;
    kind: string;
    approval_status: string;
    created_by: number;
    approved_by: number | null;
    approval_comment: string;
    assignee_user_ids: number[];
  };
  let activitiesById = new Map<string, Activity>();
  let projects: Project[] = [];
  let teams: Team[] = [];

  let selectedProjectId: number | null = null;
  let selectedTeamId: number | null = null;
  let mine = true;

  let anchor = new Date();
  let events: CalEvent[] = [];
  let showModal = false;
  let draftStart: Date | null = null;
  let draftEnd: Date | null = null;

  let modalTitle = "";
  let modalDesc = "";
  let modalKind: "TEAM" | "PERSONAL_EXTRA" = "PERSONAL_EXTRA";
  let modalMode: "CREATE" | "EDIT" = "CREATE";
  let editingId: string | null = null;

  // ✅ nuevos campos editables
  let modalStartLocal = ""; // "YYYY-MM-DDTHH:mm"
  let modalEndLocal = "";

  // --- auth guard ---
  async function waitAuthReady() {
    while (!get(auth).ready) await new Promise((r) => setTimeout(r, 50));
  }

  function toLocalInputValue(d: Date) {
    const pad = (n: number) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  function localInputToDate(v: string) {
    // v = "YYYY-MM-DDTHH:mm" -> Date local
    return new Date(v);
  }

  function toISO(d: Date) {
    return d.toISOString();
  }

  async function loadProjects() {
    projects = await api<Project[]>("/projects");
  }

  async function loadTeams() {
    teams = [];
    if (!selectedProjectId) return;
    teams = await api<Team[]>(`/projects/${selectedProjectId}/teams`);
  }

  // rango de la vista "week" (lunes-domingo)
  function weekRange(a: Date) {
    const d = new Date(a);
    const day = d.getDay(); // 0 domingo
    const diffToMon = (day === 0 ? -6 : 1) - day; // lunes
    const start = new Date(d);
    start.setDate(d.getDate() + diffToMon);
    start.setHours(0, 0, 0, 0);

    const end = new Date(start);
    end.setDate(start.getDate() + 7);
    end.setHours(0, 0, 0, 0);
    return { start, end };
  }

  async function fetchActivitiesForAnchor() {
    if (!selectedProjectId) {
      events = [];
      return;
    }

    const { start, end } = weekRange(anchor);

    const params = new URLSearchParams();
    params.set("from_iso", toISO(start));
    params.set("to_iso", toISO(end));
    params.set("mine", String(mine));
    params.set("project_id", String(selectedProjectId));
    if (selectedTeamId) params.set("team_id", String(selectedTeamId));

    const acts = await api<Activity[]>(`/activities?${params.toString()}`);

    activitiesById = new Map(acts.map((a) => [String(a.id), a]));

    events = acts.map((a) => ({
      id: String(a.id),
      title: a.title + (a.approval_status === "PENDING" ? " ⏳" : ""),
      start: a.start_at,
      end: a.end_at,
      approval_status: a.approval_status,
    }));
  }

  async function onProjectChange() {
    selectedTeamId = null;

    if (!selectedProjectId) {
      teams = [];
      events = [];
      return;
    }

    await loadTeams();
    await fetchActivitiesForAnchor();
  }

  async function onTeamChange() {
    await fetchActivitiesForAnchor();
  }

  async function onMineChange() {
    await fetchActivitiesForAnchor();
  }

  // crear actividad desde drag
  // async function handleCreate(payload: { start: Date; end: Date }) {
  //   if (!selectedProjectId) return alert("Selecciona un proyecto");

  //   await api("/activities", {
  //     method: "POST",
  //     body: JSON.stringify({
  //       project_id: selectedProjectId,
  //       team_id: selectedTeamId ?? null,
  //       category_id: null,
  //       title: "Nueva actividad",
  //       description: "",
  //       start_at: payload.start.toISOString(),
  //       end_at: payload.end.toISOString(),
  //       priority: "MEDIUM",
  //       kind: selectedTeamId ? "TEAM" : "PERSONAL_EXTRA",
  //       assignee_user_ids: []
  //     })
  //   });

  //   await fetchActivitiesForAnchor();
  // }

  function handleCreate(payload: { start: Date; end: Date }) {
    if (!selectedProjectId) return alert("Selecciona un proyecto");

    modalMode = "CREATE";
    editingId = null;

    modalTitle = "";
    modalDesc = "";
    modalKind = selectedTeamId ? "TEAM" : "PERSONAL_EXTRA";

    modalStartLocal = toLocalInputValue(payload.start);
    modalEndLocal = toLocalInputValue(payload.end);

    showModal = true;
  }

  async function saveModal() {
    if (!selectedProjectId) return;
    if (!modalTitle.trim()) return alert("Pon un título");

    const start = localInputToDate(modalStartLocal);
    const end = localInputToDate(modalEndLocal);

    if (isNaN(start.getTime()) || isNaN(end.getTime()))
      return alert("Fechas inválidas");
    if (end <= start) return alert("Fin debe ser mayor a inicio");

    if (modalMode === "CREATE") {
      await api("/activities", {
        method: "POST",
        body: JSON.stringify({
          project_id: selectedProjectId,
          team_id: modalKind === "TEAM" ? (selectedTeamId ?? null) : null,
          category_id: null,
          title: modalTitle.trim(),
          description: modalDesc.trim(),
          start_at: start.toISOString(),
          end_at: end.toISOString(),
          priority: "MEDIUM",
          kind: modalKind,
          assignee_user_ids: [],
        }),
      });
    } else {
      if (!editingId) return;

      await api(`/activities/${editingId}`, {
        method: "PATCH",
        body: JSON.stringify({
          title: modalTitle.trim(),
          description: modalDesc.trim(),
          start_at: start.toISOString(),
          end_at: end.toISOString(),
          kind: modalKind,
          team_id: modalKind === "TEAM" ? (selectedTeamId ?? null) : null,
        }),
      });
    }

    showModal = false;
    editingId = null;

    await fetchActivitiesForAnchor();
  }

  async function deleteEditing() {
    if (!editingId) return;

    const ok = confirm("¿Eliminar esta actividad?");
    if (!ok) return;

    await api(`/activities/${editingId}`, { method: "DELETE" });

    showModal = false;
    editingId = null;

    await fetchActivitiesForAnchor();
  }

  function handleEventClick(ev: CalEvent) {
    const a = activitiesById.get(String(ev.id));
    if (!a) return alert("No encontré la actividad (recarga).");

    modalMode = "EDIT";
    editingId = String(a.id);

    modalTitle = a.title ?? "";
    modalDesc = a.description ?? "";
    modalKind = (a.kind as any) || (selectedTeamId ? "TEAM" : "PERSONAL_EXTRA");

    modalStartLocal = toLocalInputValue(new Date(a.start_at));
    modalEndLocal = toLocalInputValue(new Date(a.end_at));

    showModal = true;
  }

  onMount(async () => {
    await waitAuthReady();
    const a = get(auth);
    if (!a.me) {
      goto("/login");
      return;
    }

    await loadProjects();
  });

  // cuando cambie anchor (navegación del calendario), recargar
  $: anchor,
    selectedProjectId,
    selectedTeamId,
    mine,
    fetchActivitiesForAnchor();
</script>

<h1>Scheduler (Calendario)</h1>

{#if !$auth.ready}
  <p>Cargando...</p>
{:else if !$auth.me}
  <p>Redirigiendo...</p>
{:else}
  <section
    style="display:flex; gap:12px; flex-wrap:wrap; align-items:center; margin-bottom:12px;"
  >
    <label>
      Proyecto:
      <select bind:value={selectedProjectId} on:change={onProjectChange}>
        <option value={null as any}>-- Selecciona --</option>
        {#each projects as p}
          <option value={p.id}>{p.name}</option>
        {/each}
      </select>
    </label>

    <label>
      Team:
      <select
        bind:value={selectedTeamId}
        on:change={onTeamChange}
        disabled={!teams.length}
      >
        <option value={null as any}>-- (opcional) --</option>
        {#each teams as t}
          <option value={t.id}>{t.name}</option>
        {/each}
      </select>
    </label>

    <label>
      Mine:
      <input type="checkbox" bind:checked={mine} on:change={onMineChange} />
    </label>
  </section>

  {#if !selectedProjectId}
    <p>Selecciona un proyecto para ver el calendario.</p>
  {:else}
    <IPhoneCalendar
      mode="week"
      bind:anchor
      {events}
      onCreate={handleCreate}
      onEventClick={handleEventClick}
    />
    {#if showModal}
      <div
        style="
      position:fixed;
      inset:0;
      background:rgba(0,0,0,.4);
      display:flex;
      align-items:center;
      justify-content:center;
      z-index:9999;
    "
      >
        <div
          style="background:white; padding:16px; border-radius:10px; width:min(520px, 92vw); z-index:10000;"
        >
          <h3>Nueva actividad</h3>

          <div style="display:grid; gap:10px; margin-top:10px;">
            <label>
              Tipo:
              <select bind:value={modalKind} disabled={!selectedTeamId}>
                <option value="TEAM">TEAM</option>
                <option value="PERSONAL_EXTRA">PERSONAL_EXTRA</option>
              </select>
              {#if !selectedTeamId}
                <div style="font-size:12px; opacity:.7;">
                  (Para TEAM debes elegir un Team)
                </div>
              {/if}
            </label>

            <input placeholder="Título" bind:value={modalTitle} />
            <textarea placeholder="Descripción" rows="3" bind:value={modalDesc}
            ></textarea>

            <div style="font-size:12px; opacity:.8;">
              {#if draftStart && draftEnd}
                {draftStart.toLocaleString()} → {draftEnd.toLocaleString()}
              {/if}
            </div>
            <label>
              Inicio:
              <input type="datetime-local" bind:value={modalStartLocal} />
            </label>

            <label>
              Fin:
              <input type="datetime-local" bind:value={modalEndLocal} />
            </label>

            <div style="font-size:12px; opacity:.75;">
              Tip: puedes ajustar minutos exactos aquí.
            </div>

            <div style="display:flex; gap:8px; justify-content:flex-end;">
              {#if modalMode === "EDIT"}
                <button
                  type="button"
                  on:click={deleteEditing}
                  style="margin-right:auto;"
                >
                  Eliminar
                </button>
              {/if}

              <button type="button" on:click={() => (showModal = false)}
                >Cancelar</button
              >
              <button
                type="button"
                on:click={saveModal}
                disabled={!modalTitle.trim()}
              >
                {modalMode === "EDIT" ? "Guardar cambios" : "Crear"}
              </button>
            </div>
          </div>
        </div>
      </div>
    {/if}
  {/if}
{/if}
