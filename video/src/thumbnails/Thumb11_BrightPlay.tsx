import React from "react";
import { AbsoluteFill } from "remotion";

// 테트리스 블록 색상 (오리지널 컬러)
const COLORS = {
  I: "#00d4ff",
  O: "#ffd700",
  T: "#b44dff",
  S: "#00e676",
  Z: "#ff3d3d",
  J: "#3d7aff",
  L: "#ff8c00",
};

// 실제 테트리스 보드 시뮬레이션 (10x20 중 하단 12줄만)
const BOARD: (keyof typeof COLORS | null)[][] = [
  [null, null, null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null, null, null],
  [null, null, null, null, "T", null, null, null, null, null],
  [null, null, null, "T", "T", "T", null, null, null, null],
  [null, null, null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null, "L", null],
  ["S", null, null, null, null, null, null, "L", "L", null],
  ["S", "S", null, null, "O", "O", null, "L", "J", null],
  ["Z", "S", "I", null, "O", "O", "T", "T", "J", null],
  ["Z", "Z", "I", "S", "S", "J", "J", "T", "J", "L"],
  ["O", "Z", "I", "S", "S", "Z", "J", "L", "L", "L"],
];

const CELL = 38;

const Block: React.FC<{ color: string; x: number; y: number }> = ({ color, x, y }) => (
  <div style={{
    position: "absolute",
    left: x,
    top: y,
    width: CELL - 2,
    height: CELL - 2,
    backgroundColor: color,
    borderRadius: 4,
    border: `2px solid ${color}aa`,
    boxShadow: `inset 0 0 12px ${color}66, 0 0 8px ${color}44`,
  }}>
    {/* 하이라이트 */}
    <div style={{
      position: "absolute",
      top: 3,
      left: 3,
      width: "40%",
      height: "40%",
      backgroundColor: "rgba(255,255,255,0.3)",
      borderRadius: 2,
    }} />
  </div>
);

export const Thumb11_BrightPlay: React.FC = () => {
  const boardLeft = 680;
  const boardTop = 80;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e27", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@900&display=swap');`}</style>

      {/* 배경 그라데이션 — 우하단 보라+파랑 */}
      <AbsoluteFill style={{
        background: `
          radial-gradient(ellipse at 80% 70%, rgba(100,0,255,0.25) 0%, transparent 50%),
          radial-gradient(ellipse at 20% 30%, rgba(0,100,255,0.15) 0%, transparent 50%),
          radial-gradient(ellipse at 50% 50%, rgba(0,200,255,0.08) 0%, transparent 60%)
        `,
      }} />

      {/* 배경 흩뿌리기 — 작은 테트리스 블록들 */}
      {[
        { x: 30, y: 50, c: COLORS.I, r: 15, op: 0.12 },
        { x: 150, y: 600, c: COLORS.O, r: -10, op: 0.10 },
        { x: 1100, y: 30, c: COLORS.S, r: 25, op: 0.08 },
        { x: 1050, y: 650, c: COLORS.Z, r: -20, op: 0.10 },
        { x: 550, y: 680, c: COLORS.T, r: 30, op: 0.09 },
        { x: 30, y: 350, c: COLORS.J, r: -5, op: 0.08 },
      ].map((b, i) => (
        <div key={i} style={{
          position: "absolute",
          left: b.x,
          top: b.y,
          width: 60,
          height: 60,
          backgroundColor: b.c,
          borderRadius: 8,
          opacity: b.op,
          transform: `rotate(${b.r}deg)`,
          boxShadow: `0 0 30px ${b.c}40`,
        }} />
      ))}

      {/* 왼쪽: 타이틀 영역 */}
      <div style={{
        position: "absolute",
        left: 60,
        top: 100,
        width: 580,
        display: "flex",
        flexDirection: "column",
      }}>
        {/* 배지 */}
        <div style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
          backgroundColor: "rgba(0,212,255,0.15)",
          border: "1px solid rgba(0,212,255,0.3)",
          borderRadius: 20,
          padding: "8px 20px",
          marginBottom: 30,
          width: "fit-content",
        }}>
          <span style={{ fontSize: 18 }}>🤖</span>
          <span style={{
            fontFamily: "'Inter', sans-serif",
            fontSize: 16,
            fontWeight: 900,
            color: "#00d4ff",
            letterSpacing: 1,
          }}>MADE WITH AI</span>
        </div>

        {/* TETRIS */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 120,
          color: "#ffffff",
          textShadow: `
            0 0 30px rgba(0,212,255,0.6),
            0 0 60px rgba(0,212,255,0.3),
            4px 4px 0 #001a33
          `,
          letterSpacing: 8,
          lineHeight: 1.1,
        }}>
          TETRIS
        </div>

        {/* 컬러 블록 구분선 */}
        <div style={{ display: "flex", gap: 6, margin: "24px 0" }}>
          {Object.values(COLORS).map((c, i) => (
            <div key={i} style={{
              width: 50,
              height: 8,
              borderRadius: 4,
              backgroundColor: c,
              boxShadow: `0 0 12px ${c}80`,
            }} />
          ))}
        </div>

        {/* VIBE CODING */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 44,
          color: "#b44dff",
          textShadow: `
            0 0 20px rgba(180,77,255,0.5),
            0 0 40px rgba(180,77,255,0.2),
            2px 2px 0 #1a0033
          `,
          letterSpacing: 6,
          marginBottom: 24,
        }}>
          VIBE CODING
        </div>

        {/* 서브텍스트 */}
        <div style={{
          fontFamily: "'Inter', sans-serif",
          fontSize: 22,
          color: "rgba(255,255,255,0.5)",
          fontWeight: 900,
          letterSpacing: 2,
        }}>
          BUILD YOUR OWN CLASSIC GAME
        </div>
      </div>

      {/* 오른쪽: 테트리스 보드 */}
      <div style={{
        position: "absolute",
        left: boardLeft,
        top: boardTop,
        width: CELL * 10 + 20,
        height: CELL * 12 + 20,
        backgroundColor: "rgba(0,0,30,0.7)",
        borderRadius: 12,
        border: "2px solid rgba(0,212,255,0.3)",
        padding: 10,
        boxShadow: `
          0 0 40px rgba(0,212,255,0.2),
          inset 0 0 30px rgba(0,0,0,0.5)
        `,
        transform: "perspective(800px) rotateY(-8deg) rotateX(2deg)",
      }}>
        {/* 그리드 라인 */}
        {Array.from({ length: 13 }).map((_, i) => (
          <div key={`h${i}`} style={{
            position: "absolute",
            left: 10,
            top: 10 + i * CELL,
            width: CELL * 10,
            height: 1,
            backgroundColor: "rgba(0,212,255,0.06)",
          }} />
        ))}
        {Array.from({ length: 11 }).map((_, i) => (
          <div key={`v${i}`} style={{
            position: "absolute",
            left: 10 + i * CELL,
            top: 10,
            width: 1,
            height: CELL * 12,
            backgroundColor: "rgba(0,212,255,0.06)",
          }} />
        ))}

        {/* 블록들 */}
        {BOARD.map((row, ry) =>
          row.map((cell, cx) =>
            cell ? (
              <Block
                key={`${ry}-${cx}`}
                color={COLORS[cell]}
                x={10 + cx * CELL}
                y={10 + ry * CELL}
              />
            ) : null
          )
        )}
      </div>

      {/* NEXT 프리뷰 */}
      <div style={{
        position: "absolute",
        left: boardLeft + CELL * 10 + 50,
        top: boardTop + 20,
        display: "flex",
        flexDirection: "column",
        gap: 4,
      }}>
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 14,
          color: "rgba(255,255,255,0.4)",
          marginBottom: 8,
        }}>NEXT</div>
        {/* I 피스 */}
        <div style={{ display: "flex", gap: 2 }}>
          {[0,1,2,3].map(i => (
            <div key={i} style={{
              width: 20, height: 20,
              backgroundColor: COLORS.I,
              borderRadius: 3,
              boxShadow: `0 0 6px ${COLORS.I}44`,
            }} />
          ))}
        </div>
      </div>

      {/* 하단 글로우 라인 */}
      <div style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height: 3,
        background: `linear-gradient(90deg, transparent, ${COLORS.I}, ${COLORS.T}, ${COLORS.S}, ${COLORS.Z}, transparent)`,
        boxShadow: `0 0 20px rgba(0,212,255,0.3)`,
      }} />
    </AbsoluteFill>
  );
};
