import React from "react";
import { AbsoluteFill } from "remotion";

// 보라/핑크 네온 버전
const TETRIMINO_ASCII = [
  "[][][][]", "[][]\n[][]", " []\n[][][]", "[]\n[][][]",
  "    []\n[][][]", " [][]\n[][]", "[][]\n [][]",
];

const generateRain = (count: number, seed0: number) => {
  const items: Array<{ x: number; y: number; piece: string; opacity: number; size: number }> = [];
  for (let i = 0; i < count; i++) {
    const s = i * 6173 + seed0;
    items.push({
      x: (s * 13) % 1920,
      y: ((s * 23) % 1200) - 80,
      piece: TETRIMINO_ASCII[(s * 11) % TETRIMINO_ASCII.length],
      opacity: 0.04 + ((s * 29) % 100) / 700,
      size: 14 + ((s * 7) % 10),
    });
  }
  return items;
};

const rain = generateRain(120, 99);

export const Thumb8_MatrixPurple: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#08020e", overflow: "hidden" }}>
    <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

    <AbsoluteFill style={{
      background: "radial-gradient(ellipse at 50% 45%, rgba(60,0,80,0.5) 0%, transparent 55%), radial-gradient(ellipse at 30% 70%, rgba(80,0,40,0.2) 0%, transparent 40%)",
    }} />

    {rain.map((r, i) => (
      <pre key={i} style={{
        position: "absolute", left: r.x, top: r.y,
        color: "#cc44ff", opacity: r.opacity,
        fontSize: r.size, fontFamily: "'Courier New', monospace",
        fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
        textShadow: "0 0 4px #cc44ff30",
      }}>
        {r.piece}
      </pre>
    ))}

    <AbsoluteFill style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 200,
        color: "#ffffff",
        textShadow: "0 0 40px #cc00ff, 0 0 80px #cc00ffaa, 0 0 160px #cc00ff50, 6px 6px 0 #1a0022",
        letterSpacing: 16, lineHeight: 1,
      }}>TETRIS</div>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 88,
        color: "#ff3366",
        textShadow: "0 0 25px #ff3366, 0 0 50px #ff336680, 4px 4px 0 #330011",
        letterSpacing: 10, marginTop: 16,
      }}>Original</div>
      <div style={{ display: "flex", gap: 8, margin: "44px 0" }}>
        {["#cc00ff","#ff3366","#ffff00","#00ffcc","#ff6600","#3366ff","#00ff41","#cc00ff","#ff3366","#ffff00","#00ffcc","#ff6600"].map((c, i) => (
          <div key={i} style={{ width: 36, height: 10, borderRadius: 2, backgroundColor: c, opacity: 0.9, boxShadow: `0 0 10px ${c}80` }} />
        ))}
      </div>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 76,
        color: "#00ffcc",
        textShadow: "0 0 25px #00ffcc, 0 0 50px #00ffcc80, 4px 4px 0 #002222",
        letterSpacing: 14,
      }}>VIBE CODING</div>
    </AbsoluteFill>

    <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.65) 100%)", pointerEvents: "none" }} />
    <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px)", pointerEvents: "none" }} />
  </AbsoluteFill>
);
