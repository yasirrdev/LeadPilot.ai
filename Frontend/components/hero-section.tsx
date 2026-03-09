import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"

export function HeroSection() {
  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center px-6 pt-16">
      {/* Subtle gradient background */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute left-1/2 top-0 -translate-x-1/2 h-[500px] w-[800px] rounded-full bg-accent/10 blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto max-w-4xl text-center">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-secondary/50 px-4 py-1.5 text-sm text-muted-foreground">
          <span className="h-1.5 w-1.5 rounded-full bg-accent" />
          AI-Powered Lead Management
        </div>

        <h1 className="text-balance text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
          Never Lose a Lead Again
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-pretty text-lg text-muted-foreground md:text-xl">
          LeadPilot AI automatically responds to new inquiries, qualifies leads
          and schedules calls for your business 24/7.
        </p>

        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Button asChild size="lg" className="group gap-2">
            <Link href="#demo">
              Try the Demo
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Link>
          </Button>
          <Button variant="outline" size="lg" asChild>
            <Link href="#features">Learn More</Link>
          </Button>
        </div>

        {/* Stats row */}
        <div className="mt-20 grid grid-cols-2 gap-8 border-t border-border pt-10 md:grid-cols-4">
          <div>
            <div className="text-3xl font-bold">98%</div>
            <div className="mt-1 text-sm text-muted-foreground">
              Lead Response Rate
            </div>
          </div>
          <div>
            <div className="text-3xl font-bold">24/7</div>
            <div className="mt-1 text-sm text-muted-foreground">
              Always Available
            </div>
          </div>
          <div>
            <div className="text-3xl font-bold">3x</div>
            <div className="mt-1 text-sm text-muted-foreground">
              More Conversions
            </div>
          </div>
          <div>
            <div className="text-3xl font-bold">{"<"}5s</div>
            <div className="mt-1 text-sm text-muted-foreground">
              Average Response
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
