import React from "react";
import { AbsoluteFill } from "remotion";

// 매트릭스 스타일 [] 테트리미노 비 배경
const TETRIMINO_ASCII = [
  "[][][][]",
  "[][]\n[][]",
  " []\n[][][]",
  "[]\n[][][]",
  "    []\n[][][]",
  " [][]\n[][]",
  "[][]\n [][]",
];

// 열 생성 (매트릭스 빗줄기처럼)
const generateColumns = (count: number) => {
  const cols: Array<{
    x: number;
    pieces: Array<{ piece: string; y: number; opacity: number; color: string }>;
  }> = [];

  for (let i = 0; i < count; i++) {
    const seed = i * 7919 + 31;
    const x = (seed * 13) % 1920;
    const pieceCount = 3 + (seed * 7) % 5;
    const pieces: Array<{ piece: string; y: number; opacity: number; color: string }> = [];

    for (let j = 0; j < pieceCount; j++) {
      const pseed = seed + j * 3571;
      const y = ((pseed * 23) % 1200) - 100;
      // 매트릭스 그린 계열 + 약간의 시안
      const colors = ["#00ff41", "#00cc33", "#00ff66", "#33ff77", "#00dd44", "#00ffcc", "#22ee55"];
      pieces.push({
        piece: TETRIMINO_ASCII[(pseed * 11) % TETRIMINO_ASCII.length],
        y,
        opacity: 0.06 + ((pseed * 29) % 100) / 600,
        color: colors[(pseed * 3) % colors.length],
      });
    }
    cols.push({ x, pieces });
  }
  return cols;
};

const matrixCols = generateColumns(50);

// 추가 밝은 스트림 (포커스 레인)
const brightStreams = generateColumns(12).map((col) => ({
  ...col,
  pieces: col.pieces.map((p) => ({ ...p, opacity: p.opacity * 3.5 })),
}));

export const Thumb6_MatrixRain: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#020a02", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

      {/* 배경 그라데이션 — 중앙 약간 밝게 */}
      <AbsoluteFill style={{
        background: "radial-gradient(ellipse at 50% 45%, rgba(0,40,0,0.6) 0%, transparent 60%)",
      }} />

      {/* 매트릭스 [] 비 — 어두운 레이어 */}
      {matrixCols.map((col, i) => (
        <div key={`d${i}`} style={{ position: "absolute", left: col.x, top: 0 }}>
          {col.pieces.map((p, j) => (
            <pre key={j} style={{
              position: "absolute",
              top: p.y,
              color: p.color,
              opacity: p.opacity,
              fontSize: 18,
              fontFamily: "'Courier New', monospace",
              fontWeight: "bold",
              lineHeight: 1.1,
              whiteSpace: "pre",
              margin: 0,
              textShadow: `0 0 4px ${p.color}30`,
            }}>
              {p.piece}
            </pre>
          ))}
        </div>
      ))}

      {/* 매트릭스 [] 비 — 밝은 스트림 */}
      {brightStreams.map((col, i) => (
        <div key={`b${i}`} style={{ position: "absolute", left: col.x + 40, top: 0 }}>
          {col.pieces.map((p, j) => (
            <pre key={j} style={{
              position: "absolute",
              top: p.y,
              color: p.color,
              opacity: Math.min(p.opacity, 0.45),
              fontSize: 20,
              fontFamily: "'Courier New', monospace",
              fontWeight: "bold",
              lineHeight: 1.1,
              whiteSpace: "pre",
              margin: 0,
              textShadow: `0 0 8px ${p.color}60`,
            }}>
              {p.piece}
            </pre>
          ))}
        </div>
      ))}

      {/* 중앙 타이틀 — 화면 60% 이상 */}
      <AbsoluteFill style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}>
        {/* TETRIS — 초대형 */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 200,
          color: "#ffffff",
          textShadow: `
            0 0 40px #00ffff,
            0 0 80px #00ffff80,
            0 0 120px #00ffff50,
            0 0 200px #00ffff30,
            5px 5px 0 #002233
          `,
          letterSpacing: 16,
          lineHeight: 1,
        }}>
          TETRIS
        </div>

        {/* Original — 크게 */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 88,
          color: "#ff6600",
          textShadow: `
            0 0 25px #ff6600,
            0 0 50px #ff660080,
            3px 3px 0 #331100
          `,
          letterSpacing: 10,
          marginTop: 16,
        }}>
          Original
        </div>

        {/* 구분 — 블록 라인 */}
        <div style={{ display: "flex", gap: 8, margin: "44px 0" }}>
          {["#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600",
            "#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff"].map((c, i) => (
            <div key={i} style={{
              width: 36, height: 10, borderRadius: 2,
              backgroundColor: c, opacity: 0.9,
              boxShadow: `0 0 10px ${c}80`,
            }} />
          ))}
        </div>

        {/* VIBE CODING — 크게 */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 76,
          color: "#00ff41",
          textShadow: `
            0 0 25px #00ff41,
            0 0 50px #00ff4180,
            0 0 100px #00ff4140,
            3px 3px 0 #003300
          `,
          letterSpacing: 14,
        }}>
          VIBE CODING
        </div>
      </AbsoluteFill>

      {/* 비네트 */}
      <AbsoluteFill style={{
        background: "radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.7) 100%)",
        pointerEvents: "none",
      }} />

      {/* 스캔라인 */}
      <AbsoluteFill style={{
        background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.08) 2px, rgba(0,0,0,0.08) 4px)",
        pointerEvents: "none",
      }} />
    </AbsoluteFill>
  );
};
