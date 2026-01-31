import React from "react";
import { AbsoluteFill } from "remotion";

const CELL = 46;

// 매트릭스 [] 빗줄기 배경
const TETRIMINO_ASCII = [
  "[][][][]", "[][]\n[][]", " []\n[][][]", "[]\n[][][]",
  "    []\n[][][]", " [][]\n[][]", "[][]\n [][]",
];

const generateRain = (count: number, seed0: number) => {
  const items: Array<{ x: number; y: number; piece: string; opacity: number; size: number }> = [];
  for (let i = 0; i < count; i++) {
    const s = i * 5701 + seed0;
    items.push({
      x: (s * 13) % 1920,
      y: ((s * 23) % 1200) - 80,
      piece: TETRIMINO_ASCII[(s * 11) % TETRIMINO_ASCII.length],
      opacity: 0.03 + ((s * 29) % 100) / 900,
      size: 13 + ((s * 7) % 10),
    });
  }
  return items;
};

const rain = generateRain(150, 55);

// 흩어진 3D 블록 피스들 (테두리 영역에 배치)
const PIECES = [
  { shape: [[1,1,1,1]], color: "#00ffff", x: 40, y: 60, rot: 12 },
  { shape: [[1,1],[1,1]], color: "#ffff00", x: 1700, y: 40, rot: -8 },
  { shape: [[0,1,0],[1,1,1]], color: "#cc00ff", x: 30, y: 850, rot: 18 },
  { shape: [[1,0],[1,0],[1,1]], color: "#ff6600", x: 1720, y: 800, rot: -20 },
  { shape: [[0,1],[0,1],[1,1]], color: "#3366ff", x: 180, y: 420, rot: 10 },
  { shape: [[0,1,1],[1,1,0]], color: "#00ff41", x: 1580, y: 380, rot: -12 },
  { shape: [[1,1,0],[0,1,1]], color: "#ff3366", x: 1600, y: 650, rot: 25 },
  { shape: [[1,1,1,1]], color: "#00ffff", x: 60, y: 250, rot: 90 },
  { shape: [[0,1,0],[1,1,1]], color: "#cc00ff", x: 1750, y: 220, rot: -30 },
  { shape: [[1,1],[1,1]], color: "#ffff00", x: 150, y: 680, rot: 5 },
  { shape: [[1,0],[1,0],[1,1]], color: "#ff6600", x: 1650, y: 920, rot: -15 },
  { shape: [[0,1,1],[1,1,0]], color: "#00ff41", x: 80, y: 950, rot: 22 },
  { shape: [[0,1],[0,1],[1,1]], color: "#3366ff", x: 1760, y: 520, rot: -5 },
  { shape: [[1,1,0],[0,1,1]], color: "#ff3366", x: 250, y: 140, rot: -18 },
];

const Piece: React.FC<{
  shape: number[][]; color: string; x: number; y: number; rot: number;
}> = ({ shape, color, x, y, rot }) => (
  <div style={{
    position: "absolute", left: x, top: y,
    transform: `rotate(${rot}deg)`,
    filter: `drop-shadow(0 0 14px ${color}90)`,
  }}>
    {shape.map((row, r) =>
      row.map((cell, c) => cell ? (
        <div key={`${r}-${c}`} style={{
          position: "absolute", left: c * CELL, top: r * CELL,
          width: CELL - 2, height: CELL - 2,
          backgroundColor: color,
          border: `1px solid ${color}aa`,
          borderRadius: 4,
          boxShadow: `0 0 8px ${color}60, inset 2px 2px 0 ${color}55, inset -1px -1px 0 ${color}22`,
        }} />
      ) : null)
    )}
  </div>
);

export const ThumbFinal: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#060612", overflow: "hidden" }}>
    <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

    {/* 배경 그라데이션 */}
    <AbsoluteFill style={{
      background: `
        radial-gradient(ellipse at 50% 45%, rgba(0,40,60,0.4) 0%, transparent 50%),
        radial-gradient(ellipse at 25% 70%, rgba(0,30,0,0.3) 0%, transparent 40%),
        radial-gradient(ellipse at 75% 30%, rgba(30,0,50,0.2) 0%, transparent 40%)
      `,
    }} />

    {/* 매트릭스 [] 배경 */}
    {rain.map((r, i) => (
      <pre key={i} style={{
        position: "absolute", left: r.x, top: r.y,
        color: "#00ff41", opacity: r.opacity,
        fontSize: r.size, fontFamily: "'Courier New', monospace",
        fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
        textShadow: "0 0 3px #00ff4120",
      }}>
        {r.piece}
      </pre>
    ))}

    {/* 방사형 광선 */}
    <AbsoluteFill style={{
      background: `conic-gradient(from 0deg at 50% 50%, 
        transparent 0deg, rgba(0,255,255,0.03) 10deg, transparent 20deg,
        transparent 45deg, rgba(255,0,255,0.02) 55deg, transparent 65deg,
        transparent 90deg, rgba(0,255,65,0.03) 100deg, transparent 110deg,
        transparent 135deg, rgba(255,255,0,0.02) 145deg, transparent 155deg,
        transparent 180deg, rgba(255,51,102,0.02) 190deg, transparent 200deg,
        transparent 225deg, rgba(0,255,255,0.02) 235deg, transparent 245deg,
        transparent 270deg, rgba(255,102,0,0.03) 280deg, transparent 290deg,
        transparent 315deg, rgba(204,0,255,0.02) 325deg, transparent 335deg,
        transparent 360deg)`,
    }} />

    {/* 흩어진 블록 피스들 */}
    {PIECES.map((p, i) => (
      <Piece key={i} {...p} />
    ))}

    {/* 중앙 타이틀 — 60%+ */}
    <AbsoluteFill style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{
        background: "rgba(6, 6, 18, 0.8)",
        border: "2px solid rgba(0,255,255,0.35)",
        borderRadius: 16,
        padding: "60px 100px",
        boxShadow: "0 0 60px rgba(0,255,255,0.12), 0 0 120px rgba(0,255,255,0.04), inset 0 0 60px rgba(0,0,0,0.4)",
        textAlign: "center",
        minWidth: 1100,
      }}>
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 160,
          color: "#ffffff",
          textShadow: "0 0 30px #00ffff, 0 0 60px #00ffffaa, 0 0 120px #00ffff50, 5px 5px 0 #001a2a",
          letterSpacing: 14,
          lineHeight: 1,
        }}>TETRIS</div>
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 72,
          color: "#ff6600",
          textShadow: "0 0 20px #ff6600, 0 0 40px #ff660080, 4px 4px 0 #331100",
          letterSpacing: 8,
          marginTop: 14,
        }}>Original</div>
        <div style={{ display: "flex", gap: 7, justifyContent: "center", margin: "36px 0" }}>
          {["#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600",
            "#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600"].map((c, i) => (
            <div key={i} style={{
              width: 30, height: 8, borderRadius: 2,
              backgroundColor: c, opacity: 0.85,
              boxShadow: `0 0 8px ${c}80`,
            }} />
          ))}
        </div>
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 64,
          color: "#00ff41",
          textShadow: "0 0 20px #00ff41, 0 0 40px #00ff4180, 0 0 80px #00ff4140, 4px 4px 0 #003300",
          letterSpacing: 12,
        }}>VIBE CODING</div>
      </div>
    </AbsoluteFill>

    {/* 비네트 */}
    <AbsoluteFill style={{
      background: "radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.55) 100%)",
      pointerEvents: "none",
    }} />
    {/* 스캔라인 */}
    <AbsoluteFill style={{
      background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px)",
      pointerEvents: "none",
    }} />
  </AbsoluteFill>
);
