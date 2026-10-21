import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { BreakdownTable } from "./breakdown-table";

const columns = {
  label: "Country",
  clicks: "Clicks",
  share: "Share",
};

describe("BreakdownTable", () => {
  it("renders an accessible table with formatted numbers", () => {
    render(
      <BreakdownTable
        locale="en"
        title="Countries"
        emptyLabel="No data"
        columns={columns}
        items={[
          { id: "BR", label: "Brazil", clicks: 486, share: 486 / 1063 },
          { id: "US", label: "United States", clicks: 302, share: 302 / 1063 },
        ]}
      />,
    );

    expect(screen.getByRole("table", { name: "Countries" })).toBeInTheDocument();
    expect(screen.getByRole("columnheader", { name: "Country" })).toBeInTheDocument();
    expect(screen.getByRole("rowheader", { name: "Brazil" })).toBeInTheDocument();
    expect(screen.getByRole("cell", { name: "486" })).toBeInTheDocument();
    expect(screen.getByRole("cell", { name: "45.7%" })).toBeInTheDocument();
  });

  it("supports the empty state", () => {
    render(
      <BreakdownTable
        locale="pt-BR"
        title="Países"
        emptyLabel="Sem dados"
        columns={{ label: "País", clicks: "Cliques", share: "Parte" }}
        items={[]}
      />,
    );

    expect(screen.getByText("Sem dados")).toBeInTheDocument();
    expect(screen.queryByRole("table")).not.toBeInTheDocument();
  });
});
