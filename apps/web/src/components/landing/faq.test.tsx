import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { Faq } from "./faq";

const items = Array.from({ length: 8 }, (_, index) => ({
  question: `Question ${index + 1}`,
  answer: `Answer ${index + 1}`,
}));

describe("Faq", () => {
  it("renders eight questions as native disclosure widgets", () => {
    render(<Faq title="Frequently asked questions" subtitle="Short answers." items={items} />);

    const disclosures = screen.getAllByRole("group");
    expect(disclosures).toHaveLength(8);
    expect(screen.getByText("Question 1")).toBeInTheDocument();
    expect(screen.getByText("Question 8")).toBeInTheDocument();
    expect(disclosures[0]).toHaveAttribute("open");
    expect(disclosures[1]).not.toHaveAttribute("open");
  });

  it("lets keyboard and pointer users toggle each answer", async () => {
    const user = userEvent.setup();
    render(<Faq title="Frequently asked questions" subtitle="Short answers." items={items} />);

    const summaries = screen
      .getAllByText(/^Question \d+$/)
      .map((element) => element.closest("summary"));
    expect(summaries).toHaveLength(8);
    summaries.forEach((summary) => expect(summary).not.toBeNull());

    await user.click(summaries[1] as HTMLElement);
    expect(summaries[1]?.closest("details")).toHaveAttribute("open");

    summaries[2]?.focus();
    expect(summaries[2]).toHaveFocus();
  });
});
