import React from "react";
import { AbsoluteFill } from "remotion";

// Gemini 강조 — 하단에 × GEMINI CLI
const TETRIMINO_ASCII = [
  "[][][][]", "[][]\n[][]", " []\n[][][]", "[]\n[][][]",
  "    []\n[][][]", " [][]\n[][]", "[][]\n [][]",
];

const generateRain = (count: number, seed0: number) => {
  const items: Array<{ x: number; y: number; piece: string; opacity: number; size: number }> = [];
  for (let i = 0; i < count; i++) {
    const s = i * 5431 + seed0;
    items.push({
      x: (s * 13) % 1920,
      y: ((s * 23) % 1200) - 80,
      piece: TETRIMINO_ASCII[(s * 11) % TETRIMINO_ASCII.length],
      opacity: 0.04 + ((s * 29) % 100) / 750,
      size: 14 + ((s * 7) % 10),
    });
  }
  return items;
};

const rain = generateRain(120, 77);

export const Thumb9_MatrixGemini: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#020a04", overflow: "hidden" }}>
    <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

    <AbsoluteFill style={{
      background: "radial-gradient(ellipse at 50% 40%, rgba(0,40,20,0.5) 0%, transparent 55%), radial-gradient(ellipse at 60% 80%, rgba(0,60,100,0.15) 0%, transparent 40%)",
    }} />

    {rain.map((r, i) => (
      <pre key={i} style={{
        position: "absolute", left: r.x, top: r.y,
        color: "#00ff41", opacity: r.opacity,
        fontSize: r.size, fontFamily: "'Courier New', monospace",
        fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
        textShadow: "0 0 4px #00ff4130",
      }}>
        {r.piece}
      </pre>
    ))}

    <AbsoluteFill style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 200,
        color: "#ffffff",
        textShadow: "0 0 40px #00ff41, 0 0 80px #00ff41aa, 0 0 160px #00ff4150, 6px 6px 0 #002200",
        letterSpacing: 16, lineHeight: 1,
      }}>TETRIS</div>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 88,
        color: "#ff6600",
        textShadow: "0 0 25px #ff6600, 0 0 50px #ff660080, 4px 4px 0 #331100",
        letterSpacing: 10, marginTop: 16,
      }}>Original</div>
      <div style={{ display: "flex", gap: 8, margin: "44px 0" }}>
        {["#00ff41","#00ffcc","#ffff00","#ff6600","#00ff41","#00ffcc","#ffff00","#ff6600","#00ff41","#00ffcc","#ffff00","#ff6600"].map((c, i) => (
          <div key={i} style={{ width: 36, height: 10, borderRadius: 2, backgroundColor: c, opacity: 0.9, boxShadow: `0 0 10px ${c}80` }} />
        ))}
      </div>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 68,
        color: "#00ff41",
        textShadow: "0 0 25px #00ff41, 0 0 50px #00ff4180, 4px 4px 0 #003300",
        letterSpacing: 10,
      }}>VIBE CODING</div>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 40,
        color: "#4285f4",
        textShadow: "0 0 15px #4285f4, 0 0 30px #4285f480, 3px 3px 0 #001133",
        letterSpacing: 6, marginTop: 24,
      }}>× GEMINI CLI</div>
    </AbsoluteFill>

    <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.65) 100%)", pointerEvents: "none" }} />
    <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px)", pointerEvents: "none" }} />
  </AbsoluteFill>
);
