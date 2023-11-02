"use client";

import { LoginCard } from "@/components/login-card";
import { Button } from "@/components/ui/button";

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <LoginCard></LoginCard>
    </main>
  );
}
