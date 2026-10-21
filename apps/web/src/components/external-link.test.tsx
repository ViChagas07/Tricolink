import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ExternalLink } from "./external-link";

describe("ExternalLink", () => {
  it("renders safe external URLs with a hardened rel", () => {
    render(<ExternalLink href="https://example.com">Example</ExternalLink>);

    const link = screen.getByRole("link", { name: "Example" });
    expect(link).toHaveAttribute("href", "https://example.com/");
    expect(link).toHaveAttribute("target", "_blank");
    expect(link).toHaveAttribute("rel", "noopener noreferrer nofollow ugc");
  });

  it("does not render an anchor for unsafe URLs", () => {
    render(<ExternalLink href="javascript:alert(1)">Unsafe</ExternalLink>);

    expect(screen.queryByRole("link")).not.toBeInTheDocument();
    expect(screen.getByText("Unsafe")).toBeInTheDocument();
  });
});
