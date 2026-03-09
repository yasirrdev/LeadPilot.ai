import { LeadForm } from "@/components/lead-form"

export function DemoSection() {
  return (
    <section id="demo" className="px-6 py-24">
      <div className="mx-auto max-w-6xl">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          {/* Left side - Text */}
          <div>
            <h2 className="text-balance text-3xl font-bold tracking-tight sm:text-4xl">
              See it in action
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Submit a demo inquiry and watch our AI assistant respond in
              real-time. Experience how LeadPilot AI qualifies and engages with
              your leads automatically.
            </p>
            <div className="mt-8 space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent/20 text-sm font-medium text-accent">
                  1
                </div>
                <div>
                  <div className="font-medium">Submit your inquiry</div>
                  <div className="text-sm text-muted-foreground">
                    Fill out the form with your details
                  </div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent/20 text-sm font-medium text-accent">
                  2
                </div>
                <div>
                  <div className="font-medium">AI processes your request</div>
                  <div className="text-sm text-muted-foreground">
                    Our AI analyzes and qualifies the lead
                  </div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent/20 text-sm font-medium text-accent">
                  3
                </div>
                <div>
                  <div className="font-medium">Instant response</div>
                  <div className="text-sm text-muted-foreground">
                    Receive a personalized AI reply
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right side - Form */}
          <div className="rounded-2xl border border-border bg-card p-6 shadow-xl shadow-black/5 sm:p-8">
            <div className="mb-6">
              <h3 className="text-xl font-semibold">Try the Demo</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Send a sample inquiry to test our AI
              </p>
            </div>
            <LeadForm />
          </div>
        </div>
      </div>
    </section>
  )
}
