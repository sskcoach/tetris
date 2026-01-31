import React from "react";
import { AbsoluteFill } from "remotion";

// 빽빽한 매트릭스 + 화이트 타이틀
const TETRIMINO_ASCII = [
  "[][][][]", "[][]\n[][]", " []\n[][][]", "[]\n[][][]",
  "    []\n[][][]", " [][]\n[][]", "[][]\n [][]",
];

const generateRain = (count: number, seed0: number) => {
  const items: Array<{ x: number; y: number; piece: string; opacity: number; size: number; color: string }> = [];
  const colors = ["#00ff41", "#00dd33", "#00ff66", "#33ff77", "#00bb44"];
  for (let i = 0; i < count; i++) {
    const s = i * 3299 + seed0;
    items.push({
      x: (s * 13) % 1920,
      y: ((s * 23) % 1200) - 80,
      piece: TETRIMINO_ASCII[(s * 11) % TETRIMINO_ASCII.length],
      opacity: 0.05 + ((s * 29) % 100) / 500,
      size: 12 + ((s * 7) % 14),
      color: colors[(s * 3) % colors.length],
    });
  }
  return items;
};

const rain = generateRain(200, 123); // 빽빽하게

export const Thumb10_MatrixDense: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#010a02", overflow: "hidden" }}>
    <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

    <AbsoluteFill style={{
      background: "radial-gradient(ellipse at 50% 45%, rgba(0,50,0,0.4) 0%, transparent 50%)",
    }} />

    {rain.map((r, i) => (
      <pre key={i} style={{
        position: "absolute", left: r.x, top: r.y,
        color: r.color, opacity: r.opacity,
        fontSize: r.size, fontFamily: "'Courier New', monospace",
        fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
        textShadow: `0 0 3px ${r.color}20`,
      }}>
        {r.piece}
      </pre>
    ))}

    {/* 중앙 어둡게 — 글자 가독성 */}
    <AbsoluteFill style={{
      background: "radial-gradient(ellipse 70% 55% at 50% 48%, rgba(0,0,0,0.55) 0%, transparent 100%)",
      pointerEvents: "none",
    }} />

    <AbsoluteFill style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 210,
        color: "#ffffff",
        textShadow: "0 0 30px #00ff41, 0 0 60px #00ff4180, 0 0 120px #00ff4140, 0 0 200px #00ff4120, 6px 6px 0 #001a00",
        letterSpacing: 18, lineHeight: 1,
      }}>TETRIS</div>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 92,
        color: "#ff6600",
        textShadow: "0 0 25px #ff6600, 0 0 50px #ff660080, 4px 4px 0 #331100",
        letterSpacing: 10, marginTop: 20,
      }}>Original</div>
      <div style={{ display: "flex", gap: 8, margin: "48px 0" }}>
        {["#00ff41","#ff3366","#ffff00","#00ffff","#cc00ff","#ff6600","#3366ff","#00ff41","#ff3366","#ffff00","#00ffff","#cc00ff"].map((c, i) => (
          <div key={i} style={{ width: 38, height: 10, borderRadius: 2, backgroundColor: c, opacity: 0.9, boxShadow: `0 0 10px ${c}80` }} />
        ))}
      </div>
      <div style={{
        fontFamily: "'Press Start 2P', monospace", fontSize: 80,
        color: "#00ff41",
        textShadow: "0 0 25px #00ff41, 0 0 50px #00ff4180, 0 0 100px #00ff4140, 4px 4px 0 #003300",
        letterSpacing: 14,
      }}>VIBE CODING</div>
    </AbsoluteFill>

    <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.6) 100%)", pointerEvents: "none" }} />
    <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.08) 2px, rgba(0,0,0,0.08) 4px)", pointerEvents: "none" }} />
  </AbsoluteFill>
);
