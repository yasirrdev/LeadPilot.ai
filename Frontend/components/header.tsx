import Link from "next/link"
import { Button } from "@/components/ui/button"

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              className="h-5 w-5 text-accent-foreground"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
          </div>
          <span className="text-lg font-semibold tracking-tight">LeadPilot AI</span>
        </Link>
        <nav className="hidden items-center gap-8 md:flex">
          <Link
            href="#features"
            className="text-sm text-muted-foreground transition-colors hover:text-foreground"
          >
            Features
          </Link>
          <Link
            href="#demo"
            className="text-sm text-muted-foreground transition-colors hover:text-foreground"
          >
            Demo
          </Link>
        </nav>
        <Button variant="outline" size="sm" className="hidden md:inline-flex">
          Get Started
        </Button>
      </div>
    </header>
  )
}
