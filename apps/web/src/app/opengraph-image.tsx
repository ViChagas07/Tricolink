import { ImageResponse } from "next/og";

export const alt = "Tricolink — short links with clear statistics";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        position: "relative",
        background: "#071A4D",
        color: "#FFFFFF",
        padding: "72px",
        fontFamily: "sans-serif",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 8,
          display: "flex",
        }}
      >
        <div style={{ flex: 1, background: "#0A3DA8" }} />
        <div style={{ flex: 1, background: "#FFFFFF" }} />
        <div style={{ flex: 1, background: "#D6141F" }} />
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
        <div
          style={{
            width: 64,
            height: 64,
            borderRadius: 18,
            background: "#0A3DA8",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 34,
            fontWeight: 700,
          }}
        >
          T
        </div>
        <div style={{ fontSize: 38, fontWeight: 700, letterSpacing: -1 }}>Tricolink</div>
      </div>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          marginTop: "auto",
          maxWidth: 980,
        }}
      >
        <div style={{ fontSize: 78, fontWeight: 800, lineHeight: 1.05, letterSpacing: -2 }}>
          Short links, clearly.
        </div>
        <div style={{ marginTop: 28, fontSize: 30, color: "#B9C9EF" }}>
          Free URL shortener with clear, privacy-friendly statistics.
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          right: -120,
          bottom: -160,
          width: 440,
          height: 440,
          borderRadius: 220,
          background: "#D6141F",
          opacity: 0.22,
        }}
      />
      <div
        style={{
          position: "absolute",
          right: 140,
          top: -120,
          width: 280,
          height: 280,
          borderRadius: 140,
          background: "#1450C8",
          opacity: 0.35,
        }}
      />
    </div>,
    size,
  );
}
