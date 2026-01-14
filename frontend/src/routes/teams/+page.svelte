<script lang="ts">
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { api } from "$lib/api/client";
  import { goto } from "$app/navigation";
  import { get } from "svelte/store";

  type Project = {
    id: number;
    name: string;
    description?: string;
    is_active?: boolean;
  };

  type Team = {
    id: number;
    project_id: number;
    name: string;
    color_hex: string | null;
  };

  let projects: Project[] = [];
  let teams: Team[] = [];

  let selectedProjectId: number | null = null;
  let loadingProjects = false;
  let loadingTeams = false;
  let errorMsg = "";

  // modal create/edit
  let showModal = false;
  let modalMode: "CREATE" | "EDIT" = "CREATE";
  let editingTeamId: number | null = null;

  let formName = "";
  let formColor = "#3B82F6"; // default azul

  function pickDefaultColor() {
    // simple fallback si no quieres siempre el mismo
    return "#3B82F6";
  }

  async function waitAuthReady() {
    while (!get(auth).ready) {
      await new Promise((r) => setTimeout(r, 50));
    }
  }

  onMount(async () => {
    await waitAuthReady();
    if (!get(auth).me) {
      goto("/login");
      return;
    }
    await loadProjects();
  });

  async function loadProjects() {
    errorMsg = "";
    loadingProjects = true;
    try {
      projects = await api<Project[]>("/projects");
      // autoselect 1er proyecto si existe
      if (!selectedProjectId && projects.length) {
        selectedProjectId = projects[0].id;
        await loadTeams();
      }
    } catch (e) {
      errorMsg = String(e);
    } finally {
      loadingProjects = false;
    }
  }

  async function loadTeams() {
    if (!selectedProjectId) {
      teams = [];
      return;
    }
    errorMsg = "";
    loadingTeams = true;
    try {
      teams = await api<Team[]>(`/projects/${selectedProjectId}/teams`);
    } catch (e) {
      errorMsg = String(e);
    } finally {
      loadingTeams = false;
    }
  }

  function openCreate() {
    if (!selectedProjectId) return alert("Selecciona un proyecto primero");
    modalMode = "CREATE";
    editingTeamId = null;
    formName = "";
    formColor = pickDefaultColor();
    showModal = true;
  }

  function openEdit(t: Team) {
    modalMode = "EDIT";
    editingTeamId = t.id;
    formName = t.name ?? "";
    formColor = t.color_hex ?? pickDefaultColor();
    showModal = true;
  }

  async function saveTeam() {
    if (!selectedProjectId) return;
    if (!formName.trim()) return alert("Pon un nombre de equipo");

    errorMsg = "";
    try {
      if (modalMode === "CREATE") {
        await api(`/projects/${selectedProjectId}/teams`, {
          method: "POST",
          body: JSON.stringify({
            name: formName.trim(),
            color_hex: formColor,
          }),
        });
      } else {
        if (!editingTeamId) return;
        await api(`/teams/${editingTeamId}`, {
          method: "PATCH",
          body: JSON.stringify({
            name: formName.trim(),
            color_hex: formColor,
          }),
        });
      }

      showModal = false;
      await loadTeams();
    } catch (e) {
      errorMsg = String(e);
    }
  }

  async function deleteTeam(t: Team) {
    const ok = confirm(`¿Eliminar el equipo "${t.name}"?`);
    if (!ok) return;

    errorMsg = "";
    try {
      await api(`/teams/${t.id}`, { method: "DELETE" });
      await loadTeams();
    } catch (e) {
      errorMsg = String(e);
    }
  }

  function onProjectChange() {
    loadTeams();
  }
</script>

<svelte:head>
  <title>Equipos</title>
</svelte:head>

<h1>Equipos</h1>

{#if !$auth.ready}
  <p>Cargando...</p>
{:else if !$auth.me}
  <p>Redirigiendo...</p>
{:else}
  <section class="toolbar">
    <label class="field">
      <span>Proyecto</span>
      <select
        bind:value={selectedProjectId}
        on:change={onProjectChange}
        disabled={loadingProjects}
      >
        {#if !projects.length}
          <option value={null as any}>-- Sin proyectos --</option>
        {:else}
          {#each projects as p}
            <option value={p.id}>{p.name}</option>
          {/each}
        {/if}
      </select>
    </label>

    <div class="actions">
      <button
        class="btn"
        on:click={loadTeams}
        disabled={!selectedProjectId || loadingTeams}
      >
        Refrescar
      </button>
      <button
        class="btn primary"
        on:click={openCreate}
        disabled={!selectedProjectId}
      >
        + Nuevo equipo
      </button>
    </div>
  </section>

  {#if errorMsg}
    <div class="error">{errorMsg}</div>
  {/if}

  <section class="card">
    <h2>Lista de equipos</h2>

    {#if loadingTeams}
      <p class="muted">Cargando equipos...</p>
    {:else if !selectedProjectId}
      <p class="muted">Selecciona un proyecto.</p>
    {:else if !teams.length}
      <p class="muted">No hay equipos en este proyecto.</p>
    {:else}
      <div class="grid">
        {#each teams as t (t.id)}
          <div class="team">
            <div class="team__left">
              <span class="dot" style={`background:${t.color_hex ?? "#9CA3AF"}`}
              ></span>
              <div>
                <div class="team__name">{t.name}</div>
                <div class="team__meta">ID: {t.id}</div>
              </div>
            </div>

            <div class="team__right">
              <button class="btn" on:click={() => openEdit(t)}>Editar</button>
              <button class="btn danger" on:click={() => deleteTeam(t)}
                >Eliminar</button
              >
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </section>

  {#if showModal}
    <div class="overlay" on:click={() => (showModal = false)}>
      <div class="modal" on:click|stopPropagation>
        <h3>{modalMode === "EDIT" ? "Editar equipo" : "Nuevo equipo"}</h3>

        <div class="form">
          <label class="field">
            <span>Nombre</span>
            <input bind:value={formName} placeholder="Ej. FA Team A" />
          </label>

          <label class="field">
            <span>Color</span>
            <div class="colorRow">
              <input type="color" bind:value={formColor} />
              <input class="mono" bind:value={formColor} readonly />
            </div>
          </label>

          <div class="modal__actions">
            <button class="btn" on:click={() => (showModal = false)}
              >Cancelar</button
            >
            <button
              class="btn primary"
              on:click={saveTeam}
              disabled={!formName.trim()}
            >
              {modalMode === "EDIT" ? "Guardar cambios" : "Crear"}
            </button>
          </div>

          {#if errorMsg}
            <div class="error" style="margin-top:10px;">{errorMsg}</div>
          {/if}
        </div>
      </div>
    </div>
  {/if}
{/if}

<style>
  h1 {
    margin: 0 0 12px;
  }

  .toolbar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 12px;
  }

  .field {
    display: grid;
    gap: 6px;
  }
  .field > span {
    font-size: 12px;
    opacity: 0.75;
  }

  select,
  input {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 8px 10px;
    outline: none;
  }

  .actions {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .btn {
    border: 1px solid #e5e7eb;
    background: #fff;
    border-radius: 10px;
    padding: 8px 10px;
    cursor: pointer;
  }
  .btn:hover {
    border-color: #cbd5e1;
  }
  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  .btn.primary {
    background: #111827;
    color: #fff;
    border-color: #111827;
  }
  .btn.danger {
    background: #fee2e2;
    border-color: #fecaca;
    color: #7f1d1d;
  }

  .card {
    border: 1px solid #eee;
    border-radius: 14px;
    padding: 12px;
    background: #fff;
  }

  .muted {
    opacity: 0.7;
  }

  .grid {
    display: grid;
    gap: 10px;
    margin-top: 10px;
  }

  .team {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    border: 1px solid #f1f5f9;
    border-radius: 14px;
    padding: 12px;
  }
  .team__left {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .dot {
    width: 14px;
    height: 14px;
    border-radius: 999px;
    border: 1px solid rgba(0, 0, 0, 0.08);
  }
  .team__name {
    font-weight: 800;
  }
  .team__meta {
    font-size: 12px;
    opacity: 0.7;
  }

  .team__right {
    display: flex;
    gap: 8px;
  }

  .error {
    margin-top: 10px;
    border: 1px solid #fecaca;
    background: #fff1f2;
    color: #7f1d1d;
    border-radius: 12px;
    padding: 10px;
    white-space: pre-wrap;
  }

  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  }
  .modal {
    width: min(520px, 92vw);
    background: #fff;
    border-radius: 14px;
    padding: 14px;
    border: 1px solid #eee;
  }
  .form {
    display: grid;
    gap: 10px;
    margin-top: 10px;
  }
  .colorRow {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .mono {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
      "Liberation Mono", "Courier New", monospace;
    width: 120px;
  }
  .modal__actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 8px;
  }
</style>
