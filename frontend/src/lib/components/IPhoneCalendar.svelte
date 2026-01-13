<script lang="ts">
  import type { CalEvent, ViewMode } from "$lib/calendar/types";
  import {
    addDays,
    addMonths,
    startOfWeek,
    startOfDay,
    minutesSinceStartOfDay,
    clamp,
    fmtDayLabel,
    fmtMonthTitle,
    sameDay,
  } from "$lib/calendar/date";

  export let events: CalEvent[] = [];
  export let mode: ViewMode = "week";
  export let anchor: Date = new Date();

  export let onCreate: (payload: { start: Date; end: Date }) => void;
  export let onEventClick: (ev: CalEvent) => void;

  const HOUR_HEIGHT = 56;
  const DAY_START_MIN = 0;
  const DAY_END_MIN = 24 * 60;

  $: weekStart = startOfWeek(anchor, true);
  $: weekDays = Array.from({ length: 7 }, (_, i) => addDays(weekStart, i));
  $: monthTitle = fmtMonthTitle(anchor);

  // 🔥 Clave reactiva para forzar rerender cuando cambian los events
  $: eventsKey = events
    .map((e) => `${e.id}|${e.start}|${e.end}|${e.approval_status ?? ""}`)
    .join("~");

  function prev() {
    anchor = mode === "week" ? addDays(anchor, -7) : addMonths(anchor, -1);
  }
  function next() {
    anchor = mode === "week" ? addDays(anchor, 7) : addMonths(anchor, 1);
  }
  function today() {
    anchor = new Date();
  }

  function eventsForDay(day: Date) {
    return events
      .filter((ev) => {
        const s = new Date(ev.start);
        const e = new Date(ev.end);
        const d0 = startOfDay(day);
        const d1 = addDays(d0, 1);
        return e > d0 && s < d1;
      })
      .map((ev) => {
        const s = new Date(ev.start);
        const e = new Date(ev.end);

        const top =
          (clamp(minutesSinceStartOfDay(s), DAY_START_MIN, DAY_END_MIN) / 60) *
          HOUR_HEIGHT;

        const endMin = clamp(
          minutesSinceStartOfDay(e),
          DAY_START_MIN,
          DAY_END_MIN
        );
        const startMin = clamp(
          minutesSinceStartOfDay(s),
          DAY_START_MIN,
          DAY_END_MIN
        );

        const height = Math.max(18, ((endMin - startMin) / 60) * HOUR_HEIGHT);

        return { ev, top, height };
      });
  }

  // drag-to-create
  let dragging = false;
  let dragDay: Date | null = null;
  let dragStartMin = 0;
  let dragEndMin = 0;

  function minFromClientY(container: HTMLElement, clientY: number) {
    const rect = container.getBoundingClientRect();
    const y = clamp(clientY - rect.top, 0, rect.height);
    const minutes = Math.round(((y / rect.height) * 24 * 60) / 15) * 15; // snap 15
    return clamp(minutes, 0, 24 * 60);
  }

  function onMouseDown(day: Date, e: MouseEvent) {
    const el = e.currentTarget as HTMLElement;

    dragging = true;
    dragDay = day;
    dragStartMin = minFromClientY(el, e.clientY);
    dragEndMin = dragStartMin + 30;
  }

  function onMouseMove(day: Date, e: MouseEvent) {
    if (!dragging || !dragDay) return;
    if (!sameDay(day, dragDay)) return;

    const el = e.currentTarget as HTMLElement;
    dragEndMin = minFromClientY(el, e.clientY);
  }

  function onMouseUp() {
    if (!dragging || !dragDay) return;
    dragging = false;

    const a = Math.min(dragStartMin, dragEndMin);
    const b = Math.max(dragStartMin, dragEndMin);

    const start = new Date(dragDay);
    start.setHours(0, a, 0, 0);

    const end = new Date(dragDay);
    end.setHours(0, b, 0, 0);

    if (onCreate && b - a >= 15) onCreate({ start, end });
    dragDay = null;
  }
</script>

<div class="cal">
  <header class="cal__header">
    <div class="cal__left">
      <button class="btn" on:click={prev}>‹</button>
      <button class="btn" on:click={next}>›</button>
      <button class="btn ghost" on:click={today}>Hoy</button>
    </div>

    <div class="cal__title">{monthTitle}</div>

    <div class="cal__right">
      <button
        class="seg {mode === 'month' ? 'on' : ''}"
        on:click={() => (mode = "month")}
      >
        Mes
      </button>
      <button
        class="seg {mode === 'week' ? 'on' : ''}"
        on:click={() => (mode = "week")}
      >
        Semana
      </button>
    </div>
  </header>

  {#if mode === "month"}
    <div class="month">
      <p class="muted">
        MVP: aquí meteremos la vista mes “iPhone” (grid + dots). Ahorita la
        semana es la pro.
      </p>
    </div>
  {:else}
    <!-- ✅ Fuerza rerender del week cuando llegan events -->
    {#key eventsKey}
      <div class="week">
        <div class="week__top">
          <div class="timecol"></div>
          {#each weekDays as d}
            <div class="dayhead {sameDay(d, new Date()) ? 'today' : ''}">
              <div class="dow">{fmtDayLabel(d)}</div>
            </div>
          {/each}
        </div>

        <div class="week__body" on:mouseup={onMouseUp}>
          <div class="timecol">
            {#each Array.from({ length: 24 }, (_, h) => h) as h}
              <div class="tick">{String(h).padStart(2, "0")}:00</div>
            {/each}
          </div>

          {#each weekDays as day (day.toDateString())}
            <div
              class="daycol"
              role="gridcell"
              tabindex="0"
              on:mousedown={(e) => onMouseDown(day, e)}
              on:mousemove={(e) => onMouseMove(day, e)}
            >
              <!-- hour lines -->
              {#each Array.from({ length: 24 }, (_, h) => h) as h}
                <div class="hourline" style={`top:${h * HOUR_HEIGHT}px;`}></div>
              {/each}

              <!-- selection -->
              {#if dragging && dragDay && sameDay(day, dragDay)}
                {#key dragStartMin + ":" + dragEndMin}
                  <div
                    class="select"
                    style={`top:${(Math.min(dragStartMin, dragEndMin) / 60) * HOUR_HEIGHT}px;height:${Math.max(
                      18,
                      (Math.abs(dragEndMin - dragStartMin) / 60) * HOUR_HEIGHT
                    )}px;`}
                  />
                {/key}
              {/if}

              <!-- events -->
              {#each eventsForDay(day) as item (day.toDateString() + ":" + String(item.ev.id))}
                <button
                  class="event {item.ev.approval_status === 'PENDING'
                    ? 'pending'
                    : ''}"
                  style={`top:${item.top}px;height:${item.height}px;`}
                  on:click={() => onEventClick?.(item.ev)}
                  type="button"
                >
                  <div class="event__title">{item.ev.title}</div>
                  {#if item.ev.approval_status === "PENDING"}
                    <div class="event__sub">⏳ Pendiente</div>
                  {/if}
                </button>
              {/each}
            </div>
          {/each}
        </div>
      </div>
    {/key}
  {/if}
</div>

<style>
  .cal {
    max-width: 1100px;
    margin: 0 auto;
  }
  .cal__header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 6px;
  }
  .cal__left,
  .cal__right {
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .cal__title {
    flex: 1;
    text-align: center;
    font-weight: 700;
  }

  .btn {
    padding: 6px 10px;
    border: 1px solid #ddd;
    background: #fff;
    border-radius: 10px;
    cursor: pointer;
  }
  .btn.ghost {
    background: transparent;
  }
  .seg {
    padding: 6px 10px;
    border: 1px solid #ddd;
    background: #fff;
    border-radius: 999px;
    cursor: pointer;
  }
  .seg.on {
    border-color: #111;
  }

  .week__top {
    display: grid;
    grid-template-columns: 64px repeat(7, 1fr);
    gap: 0;
  }
  .dayhead {
    padding: 8px;
    border-bottom: 1px solid #eee;
  }
  .dayhead.today .dow {
    font-weight: 800;
  }
  .dow {
    font-size: 12px;
    opacity: 0.8;
  }

  .week__body {
    display: grid;
    grid-template-columns: 64px repeat(7, 1fr);
  }
  .timecol {
    border-right: 1px solid #eee;
  }
  .tick {
    height: 56px;
    font-size: 11px;
    padding: 6px 6px 0;
    opacity: 0.6;
  }

  .daycol {
    position: relative;
    height: calc(24 * 56px);
    border-right: 1px solid #f0f0f0;
    background: #fff;
    outline: none;
  }
  .hourline {
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background: #f3f3f3;
  }
  .select {
    position: absolute;
    left: 6px;
    right: 6px;
    background: rgba(0, 0, 0, 0.06);
    border: 1px dashed #bbb;
    border-radius: 10px;
    z-index: 1;
  }

  .event {
    position: absolute;
    left: 6px;
    right: 6px;
    background: #111;
    color: #fff;
    border: 0;
    border-radius: 12px;
    padding: 8px;
    text-align: left;
    z-index: 2;
    cursor: pointer;
  }
  .event.pending {
    background: #444;
  }
  .event__title {
    font-size: 12px;
    font-weight: 700;
    line-height: 1.1;
  }
  .event__sub {
    font-size: 11px;
    opacity: 0.85;
    margin-top: 4px;
  }

  .muted {
    opacity: 0.7;
    padding: 12px;
  }
</style>
