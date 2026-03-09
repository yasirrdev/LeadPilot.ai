import { Zap, MessageSquare, Calendar } from "lucide-react"

const features = [
  {
    icon: Zap,
    title: "Instant Lead Response",
    description:
      "Automatically replies to every new inquiry within seconds, ensuring no lead goes unanswered.",
  },
  {
    icon: MessageSquare,
    title: "Lead Qualification",
    description:
      "AI asks smart questions to qualify potential customers and prioritize high-value opportunities.",
  },
  {
    icon: Calendar,
    title: "Automatic Scheduling",
    description:
      "Integrates with your calendar to book calls instantly, eliminating back-and-forth emails.",
  },
]

export function FeaturesSection() {
  return (
    <section id="features" className="border-t border-border px-6 py-24">
      <div className="mx-auto max-w-6xl">
        <div className="text-center">
          <h2 className="text-balance text-3xl font-bold tracking-tight sm:text-4xl">
            Powerful features for modern teams
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-pretty text-lg text-muted-foreground">
            Everything you need to capture, qualify, and convert leads
            automatically.
          </p>
        </div>

        <div className="mt-16 grid gap-8 md:grid-cols-3">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group relative rounded-2xl border border-border bg-card p-6 transition-colors hover:border-accent/50 hover:bg-card/80"
            >
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-accent/10 transition-colors group-hover:bg-accent/20">
                <feature.icon className="h-6 w-6 text-accent" />
              </div>
              <h3 className="text-lg font-semibold">{feature.title}</h3>
              <p className="mt-2 text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
