import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="mr-4">
        <Button asChild>
          <Link href="/createuser">Create User</Link>
        </Button>
      </div>
      <div className="mr-4">
        <Button asChild>
          <Link href="/login">Login</Link>
        </Button>
      </div>
    </div>
  );
}
