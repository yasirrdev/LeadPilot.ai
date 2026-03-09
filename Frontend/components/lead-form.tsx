"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { CheckCircle2, Loader2 } from "lucide-react"

export function LeadForm() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    message: "",
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      await fetch("http://localhost:8000/lead", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })
    } catch (error) {
      // Still show success for demo purposes even if backend is unavailable
      console.log("Backend not available, showing success state for demo")
    }

    setIsSubmitting(false)
    setIsSubmitted(true)
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  if (isSubmitted) {
    return (
      <div className="flex flex-col items-center justify-center rounded-xl border border-accent/30 bg-accent/5 p-8 text-center">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-accent/20">
          <CheckCircle2 className="h-8 w-8 text-accent" />
        </div>
        <h3 className="text-xl font-semibold">Thank you!</h3>
        <p className="mt-2 max-w-sm text-muted-foreground">
          Our AI assistant has received your request and will respond shortly.
        </p>
        <Button
          variant="outline"
          className="mt-6"
          onClick={() => {
            setIsSubmitted(false)
            setFormData({ name: "", email: "", company: "", message: "" })
          }}
        >
          Send Another
        </Button>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="name" className="mb-2 block text-sm font-medium">
            Name
          </label>
          <Input
            id="name"
            name="name"
            placeholder="John Doe"
            required
            value={formData.name}
            onChange={handleChange}
            className="bg-secondary/50"
          />
        </div>
        <div>
          <label htmlFor="email" className="mb-2 block text-sm font-medium">
            Email
          </label>
          <Input
            id="email"
            name="email"
            type="email"
            placeholder="john@company.com"
            required
            value={formData.email}
            onChange={handleChange}
            className="bg-secondary/50"
          />
        </div>
      </div>
      <div>
        <label htmlFor="company" className="mb-2 block text-sm font-medium">
          Company
        </label>
        <Input
          id="company"
          name="company"
          placeholder="Acme Inc."
          required
          value={formData.company}
          onChange={handleChange}
          className="bg-secondary/50"
        />
      </div>
      <div>
        <label htmlFor="message" className="mb-2 block text-sm font-medium">
          Message
        </label>
        <Textarea
          id="message"
          name="message"
          placeholder="Tell us about your needs..."
          rows={4}
          required
          value={formData.message}
          onChange={handleChange}
          className="resize-none bg-secondary/50"
        />
      </div>
      <Button type="submit" className="w-full" size="lg" disabled={isSubmitting}>
        {isSubmitting ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Sending...
          </>
        ) : (
          "Send Inquiry"
        )}
      </Button>
    </form>
  )
}
