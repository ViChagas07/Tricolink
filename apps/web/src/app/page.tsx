export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-6">
      <div className="max-w-md text-center">
        <p className="text-sm font-medium tracking-[0.2em] text-muted-foreground uppercase">
          Tricolink
        </p>
        <h1 className="mt-4 text-4xl font-bold tracking-tight text-foreground">
          Short links, clearly.
        </h1>
        <p className="mt-4 text-base text-muted-foreground">
          The web scaffold is running. The URL shortener arrives in the next phases.
        </p>
      </div>
    </main>
  );
}
