import React from "react";
import { AbsoluteFill } from "remotion";

// 미니멀 볼드 — 큰 타이포 + 장식 블록
const CELL = 40;

const decoBlocks = [
  // 왼쪽 상단
  { x: 40, y: 60, w: 4, h: 1, color: "#00ffff", opacity: 0.7 },
  { x: 40, y: 120, w: 2, h: 2, color: "#ffff00", opacity: 0.5 },
  // 왼쪽 하단
  { x: 60, y: 880, w: 1, h: 4, color: "#cc00ff", opacity: 0.6 },
  { x: 120, y: 920, w: 3, h: 1, color: "#00ff41", opacity: 0.5 },
  // 오른쪽 상단
  { x: 1720, y: 40, w: 1, h: 4, color: "#ff3366", opacity: 0.6 },
  { x: 1620, y: 80, w: 2, h: 2, color: "#3366ff", opacity: 0.5 },
  // 오른쪽 하단
  { x: 1660, y: 860, w: 4, h: 1, color: "#ff6600", opacity: 0.7 },
  { x: 1740, y: 740, w: 2, h: 2, color: "#00ffff", opacity: 0.4 },
  // 산재
  { x: 300, y: 300, w: 1, h: 1, color: "#ff3366", opacity: 0.2 },
  { x: 1500, y: 400, w: 1, h: 1, color: "#00ff41", opacity: 0.2 },
  { x: 400, y: 700, w: 1, h: 1, color: "#cc00ff", opacity: 0.15 },
  { x: 1400, y: 650, w: 1, h: 1, color: "#ffff00", opacity: 0.15 },
];

export const Thumb5_MinimalBold: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#050510", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

      {/* 미세한 배경 그라데이션 */}
      <AbsoluteFill style={{
        background: "radial-gradient(ellipse at 50% 45%, rgba(20,20,60,1) 0%, rgba(5,5,16,1) 70%)",
      }} />

      {/* 장식 블록들 */}
      {decoBlocks.map((b, i) => (
        <div key={i} style={{
          position: "absolute",
          left: b.x, top: b.y,
          width: b.w * CELL - 2,
          height: b.h * CELL - 2,
          display: "flex", flexWrap: "wrap",
        }}>
          {Array.from({ length: b.w * b.h }, (_, j) => (
            <div key={j} style={{
              width: CELL - 3, height: CELL - 3,
              margin: 1,
              backgroundColor: b.color,
              borderRadius: 3,
              opacity: b.opacity,
              boxShadow: `0 0 8px ${b.color}40`,
            }} />
          ))}
        </div>
      ))}

      {/* 메인 타이포 */}
      <AbsoluteFill style={{
        display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center",
      }}>
        {/* TETRIS */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 180,
          fontWeight: 900,
          color: "#ffffff",
          textShadow: "0 0 40px #00ffff, 0 0 80px #00ffff60, 0 0 120px #00ffff30",
          letterSpacing: 16,
          lineHeight: 1,
        }}>
          TETRIS
        </div>

        {/* Original */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 64,
          color: "#ff6600",
          textShadow: "0 0 20px #ff6600, 0 0 40px #ff660060",
          letterSpacing: 8,
          marginTop: 20,
        }}>
          Original
        </div>

        {/* 구분선 — 네온 블록 라인 */}
        <div style={{
          display: "flex", gap: 6, margin: "50px 0",
        }}>
          {["#00ffff", "#ff3366", "#ffff00", "#00ff41", "#cc00ff", "#3366ff", "#ff6600",
            "#00ffff", "#ff3366", "#ffff00", "#00ff41", "#cc00ff", "#3366ff", "#ff6600",
            "#00ffff", "#ff3366"].map((c, i) => (
            <div key={i} style={{
              width: 28, height: 8, borderRadius: 2,
              backgroundColor: c,
              opacity: 0.8,
              boxShadow: `0 0 8px ${c}80`,
            }} />
          ))}
        </div>

        {/* VIBE CODING */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 56,
          color: "#00ff41",
          textShadow: "0 0 20px #00ff41, 0 0 40px #00ff4160",
          letterSpacing: 16,
        }}>
          VIBE CODING
        </div>
      </AbsoluteFill>

      {/* 스캔라인 */}
      <AbsoluteFill style={{
        background: "repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.04) 3px, rgba(0,0,0,0.04) 6px)",
        pointerEvents: "none",
      }} />
    </AbsoluteFill>
  );
};
