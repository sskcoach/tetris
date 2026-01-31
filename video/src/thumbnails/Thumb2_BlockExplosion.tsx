import React from "react";
import { AbsoluteFill } from "remotion";

const CELL = 44;

const PIECES = [
  { shape: [[1,1,1,1]], color: "#00ffff", x: 150, y: 120, rot: 15 },
  { shape: [[1,1],[1,1]], color: "#ffff00", x: 1600, y: 150, rot: -10 },
  { shape: [[0,1,0],[1,1,1]], color: "#cc00ff", x: 100, y: 800, rot: 20 },
  { shape: [[1,0],[1,0],[1,1]], color: "#ff6600", x: 1650, y: 750, rot: -25 },
  { shape: [[0,1],[0,1],[1,1]], color: "#3366ff", x: 300, y: 500, rot: 12 },
  { shape: [[0,1,1],[1,1,0]], color: "#00ff41", x: 1500, y: 450, rot: -8 },
  { shape: [[1,1,0],[0,1,1]], color: "#ff3366", x: 1350, y: 850, rot: 30 },
  { shape: [[1,1,1,1]], color: "#00ffff", x: 50, y: 350, rot: 90 },
  { shape: [[0,1,0],[1,1,1]], color: "#cc00ff", x: 1700, y: 550, rot: -45 },
  { shape: [[1,1],[1,1]], color: "#ffff00", x: 800, y: 50, rot: 5 },
  { shape: [[1,0],[1,0],[1,1]], color: "#ff6600", x: 750, y: 900, rot: -15 },
  { shape: [[0,1,1],[1,1,0]], color: "#00ff41", x: 1100, y: 80, rot: 18 },
];

const Piece: React.FC<{
  shape: number[][]; color: string; x: number; y: number; rot: number; opacity: number;
}> = ({ shape, color, x, y, rot, opacity }) => (
  <div style={{
    position: "absolute", left: x, top: y,
    transform: `rotate(${rot}deg)`,
    opacity,
    filter: `drop-shadow(0 0 12px ${color}80)`,
  }}>
    {shape.map((row, r) =>
      row.map((cell, c) => cell ? (
        <div key={`${r}-${c}`} style={{
          position: "absolute", left: c * CELL, top: r * CELL,
          width: CELL - 2, height: CELL - 2,
          backgroundColor: color,
          border: `1px solid ${color}aa`,
          borderRadius: 4,
          boxShadow: `0 0 10px ${color}60, inset 2px 2px 0 ${color}44`,
        }} />
      ) : null)
    )}
  </div>
);

export const Thumb2_BlockExplosion: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#080818", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

      {/* 방사형 광선 */}
      <AbsoluteFill style={{
        background: `
          radial-gradient(ellipse at center, rgba(0,100,200,0.25) 0%, transparent 50%),
          conic-gradient(from 0deg at 50% 50%, 
            transparent 0deg, rgba(0,255,255,0.06) 15deg, transparent 30deg,
            transparent 60deg, rgba(255,0,255,0.04) 75deg, transparent 90deg,
            transparent 120deg, rgba(0,255,65,0.05) 135deg, transparent 150deg,
            transparent 180deg, rgba(255,255,0,0.04) 195deg, transparent 210deg,
            transparent 240deg, rgba(255,51,102,0.05) 255deg, transparent 270deg,
            transparent 300deg, rgba(0,255,255,0.04) 315deg, transparent 330deg,
            transparent 360deg)
        `,
      }} />

      {/* 흩어진 블록들 */}
      {PIECES.map((p, i) => (
        <Piece key={i} {...p} opacity={0.6 + (i % 3) * 0.15} />
      ))}

      {/* 중앙 타이틀 */}
      <AbsoluteFill style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{
          background: "rgba(8, 8, 24, 0.85)",
          border: "2px solid rgba(0,255,255,0.4)",
          borderRadius: 12,
          padding: "50px 90px",
          boxShadow: "0 0 60px rgba(0,255,255,0.15), 0 0 120px rgba(0,255,255,0.05), inset 0 0 40px rgba(0,0,0,0.5)",
          textAlign: "center",
        }}>
          <div style={{
            fontFamily: "'Press Start 2P', monospace",
            fontSize: 120,
            color: "#ffffff",
            textShadow: "0 0 20px #00ffff, 0 0 40px #00ffff80, 0 0 80px #00ffff40, 3px 3px 0 #001122",
            letterSpacing: 10,
          }}>
            TETRIS
          </div>
          <div style={{
            fontFamily: "'Press Start 2P', monospace",
            fontSize: 48,
            color: "#ff6600",
            textShadow: "0 0 15px #ff6600, 0 0 30px #ff660080, 2px 2px 0 #220800",
            letterSpacing: 4,
            marginTop: 8,
          }}>
            Original
          </div>
          <div style={{
            width: "100%", height: 2,
            background: "linear-gradient(90deg, transparent, #00ff41, transparent)",
            margin: "30px 0",
          }} />
          <div style={{
            fontFamily: "'Press Start 2P', monospace",
            fontSize: 44,
            color: "#00ff41",
            textShadow: "0 0 15px #00ff41, 0 0 30px #00ff4180, 2px 2px 0 #002200",
            letterSpacing: 12,
          }}>
            VIBE CODING
          </div>
        </div>
      </AbsoluteFill>

      {/* 스캔라인 */}
      <AbsoluteFill style={{
        background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 4px)",
        pointerEvents: "none",
      }} />
      <AbsoluteFill style={{
        background: "radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.5) 100%)",
        pointerEvents: "none",
      }} />
    </AbsoluteFill>
  );
};
