import { RecordList } from "@/components/records/record-list";

export default function RecordsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Records</h1>
        <p className="text-muted-foreground mt-2">
          Manage your records. New records are automatically processed by the background worker.
        </p>
      </div>
      <RecordList />
    </div>
  );
}
