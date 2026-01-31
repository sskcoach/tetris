import React from "react";
import { AbsoluteFill } from "remotion";

const TETRIMINO_ASCII = [
  "[][][][]", "[][]\n[][]", " []\n[][][]", "[]\n[][][]",
  "    []\n[][][]", " [][]\n[][]", "[][]\n [][]",
];

const generateRain = (count: number, seed0: number) => {
  const items: Array<{ x: number; y: number; piece: string; opacity: number; size: number; color: string }> = [];
  const colors = ["#00ff41", "#00cc33", "#00ff66", "#33ff77", "#00dd44", "#00ffcc", "#22ee55", "#44ff88"];
  for (let i = 0; i < count; i++) {
    const s = i * 7919 + seed0;
    items.push({
      x: (s * 13) % 1920,
      y: ((s * 23) % 1300) - 150,
      piece: TETRIMINO_ASCII[(s * 11) % TETRIMINO_ASCII.length],
      opacity: 0.25 + ((s * 29) % 100) / 200,
      size: 36 + ((s * 7) % 30),
      color: colors[(s * 3) % colors.length],
    });
  }
  return items;
};

// 밝은 하이라이트 스트림
const generateBright = (count: number, seed0: number) => {
  const items: Array<{ x: number; y: number; piece: string; opacity: number; size: number; color: string }> = [];
  for (let i = 0; i < count; i++) {
    const s = i * 3571 + seed0;
    items.push({
      x: (s * 17) % 1920,
      y: ((s * 31) % 1300) - 150,
      piece: TETRIMINO_ASCII[(s * 13) % TETRIMINO_ASCII.length],
      opacity: 0.55 + ((s * 23) % 100) / 300,
      size: 42 + ((s * 11) % 24),
      color: "#00ff41",
    });
  }
  return items;
};

const rain = generateRain(100, 31);
const bright = generateBright(20, 67);

export const Thumb6v2: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#020a02", overflow: "hidden" }}>
    <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

    {/* 배경 글로우 */}
    <AbsoluteFill style={{
      background: "radial-gradient(ellipse at 50% 45%, rgba(0,60,0,0.5) 0%, transparent 55%)",
    }} />

    {/* 매트릭스 [] 배경 — 크고 잘 보이게 */}
    {rain.map((r, i) => (
      <pre key={`r${i}`} style={{
        position: "absolute", left: r.x, top: r.y,
        color: r.color, opacity: r.opacity,
        fontSize: r.size, fontFamily: "'Courier New', monospace",
        fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
        textShadow: `0 0 10px ${r.color}60, 0 0 20px ${r.color}30`,
      }}>
        {r.piece}
      </pre>
    ))}

    {/* 밝은 스트림 */}
    {bright.map((r, i) => (
      <pre key={`b${i}`} style={{
        position: "absolute", left: r.x, top: r.y,
        color: r.color, opacity: r.opacity,
        fontSize: r.size, fontFamily: "'Courier New', monospace",
        fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
        textShadow: `0 0 10px ${r.color}80, 0 0 20px ${r.color}40`,
      }}>
        {r.piece}
      </pre>
    ))}

    {/* 중앙 어두운 영역 — 텍스트 가독성 */}
    <AbsoluteFill style={{
      background: "radial-gradient(ellipse 65% 50% at 50% 48%, rgba(0,0,0,0.6) 0%, transparent 100%)",
      pointerEvents: "none",
    }} />

    {/* 타이틀 — TETRIS + VIBE CODING 둘 다 크게 */}
    <AbsoluteFill style={{
      display: "flex", flexDirection: "column",
      alignItems: "center", justifyContent: "center", gap: 40,
    }}>
      <div style={{
        fontFamily: "'Press Start 2P', monospace",
        fontSize: 200,
        color: "#ffffff",
        textShadow: `
          0 0 40px #00ffff,
          0 0 80px #00ffffaa,
          0 0 140px #00ffff60,
          0 0 220px #00ffff30,
          6px 6px 0 #002233
        `,
        letterSpacing: 16, lineHeight: 1,
      }}>TETRIS</div>

      {/* 블록 구분선 */}
      <div style={{ display: "flex", gap: 8 }}>
        {["#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600",
          "#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600"].map((c, i) => (
          <div key={i} style={{
            width: 34, height: 10, borderRadius: 2,
            backgroundColor: c, opacity: 0.9,
            boxShadow: `0 0 10px ${c}80`,
          }} />
        ))}
      </div>

      <div style={{
        fontFamily: "'Press Start 2P', monospace",
        fontSize: 140,
        color: "#00ff41",
        textShadow: `
          0 0 35px #00ff41,
          0 0 70px #00ff41aa,
          0 0 120px #00ff4160,
          0 0 200px #00ff4130,
          5px 5px 0 #003300
        `,
        letterSpacing: 12, lineHeight: 1,
      }}>VIBE CODING</div>
    </AbsoluteFill>

    {/* 비네트 */}
    <AbsoluteFill style={{
      background: "radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.6) 100%)",
      pointerEvents: "none",
    }} />
    {/* 스캔라인 */}
    <AbsoluteFill style={{
      background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px)",
      pointerEvents: "none",
    }} />
  </AbsoluteFill>
);
