export function startOfDay(d: Date) {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate(), 0, 0, 0, 0);
}
export function addDays(d: Date, n: number) {
  const x = new Date(d);
  x.setDate(x.getDate() + n);
  return x;
}
export function addMonths(d: Date, n: number) {
  return new Date(d.getFullYear(), d.getMonth() + n, 1);
}
export function startOfWeek(d: Date, weekStartsOnMonday = true) {
  const x = startOfDay(d);
  const day = x.getDay(); // 0=Sun
  const delta = weekStartsOnMonday ? (day === 0 ? -6 : 1 - day) : -day;
  return addDays(x, delta);
}
export function sameDay(a: Date, b: Date) {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}
export function minutesSinceStartOfDay(d: Date) {
  return d.getHours() * 60 + d.getMinutes();
}
export function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n));
}
export function fmtDayLabel(d: Date) {
  return d.toLocaleDateString(undefined, { weekday: "short", day: "2-digit" });
}
export function fmtMonthTitle(d: Date) {
  return d.toLocaleDateString(undefined, { month: "long", year: "numeric" });
}
