export type ApprovalStatus = "PENDING" | "APPROVED" | "REJECTED";

export type CalEvent = {
  id: string | number;
  title: string;
  start: string;
  end: string;
  approval_status?: ApprovalStatus;

  // 👇 nuevos
  team_id?: number | null;
  created_by?: number | null;
  kind?: "TEAM" | "PERSONAL_EXTRA" | string;
};