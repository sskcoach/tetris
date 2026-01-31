import React from "react";
import { AbsoluteFill } from "remotion";

const COLORS = ["#00ffff", "#ffff00", "#cc00ff", "#00ff41", "#ff3366", "#3366ff", "#ff6600"];
const CELL = 48;
const COLS = 10;
const ROWS = 20;

// 미리 채워진 보드 (하단 12줄 + 불규칙)
const generateBoard = (): (string | null)[][] => {
  const board: (string | null)[][] = Array.from({ length: ROWS }, () => Array(COLS).fill(null));
  for (let r = 8; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const hash = Math.sin(r * 31 + c * 17) * 10000;
      if (hash - Math.floor(hash) > 0.15 || r > 14) {
        board[r][c] = COLORS[Math.abs(Math.floor(hash * 7)) % COLORS.length];
      }
    }
  }
  // I-piece 떨어지는 중 (col 3, row 2~5)
  for (let i = 0; i < 4; i++) board[2 + i][3] = "#00ffff";
  return board;
};

const BOARD = generateBoard();

export const Thumb1_NeonBoard: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a1a", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

      {/* 배경 그라데이션 */}
      <AbsoluteFill style={{
        background: "radial-gradient(ellipse at 30% 50%, rgba(0,100,150,0.3) 0%, transparent 50%), radial-gradient(ellipse at 70% 60%, rgba(100,0,150,0.2) 0%, transparent 50%)",
      }} />

      {/* 테트리스 보드 (왼쪽) */}
      <div style={{
        position: "absolute",
        left: 80,
        top: (1080 - ROWS * CELL) / 2 - 20,
      }}>
        {/* 보드 배경 */}
        <div style={{
          position: "absolute",
          left: -6,
          top: -6,
          width: COLS * CELL + 12,
          height: ROWS * CELL + 12,
          border: "2px solid #00ffff44",
          borderRadius: 6,
          background: "rgba(0,0,0,0.5)",
          boxShadow: "0 0 40px rgba(0,255,255,0.1)",
        }} />
        {/* 그리드 */}
        {BOARD.map((row, r) =>
          row.map((color, c) => color ? (
            <div key={`${r}-${c}`} style={{
              position: "absolute",
              left: c * CELL,
              top: r * CELL,
              width: CELL - 2,
              height: CELL - 2,
              backgroundColor: color,
              border: `1px solid ${color}88`,
              borderRadius: 3,
              boxShadow: `0 0 8px ${color}60, inset 1px 1px 0 ${color}44`,
            }} />
          ) : null)
        )}
        {/* 그리드 라인 */}
        {Array.from({ length: COLS + 1 }, (_, i) => (
          <div key={`v${i}`} style={{
            position: "absolute", left: i * CELL, top: 0,
            width: 1, height: ROWS * CELL,
            backgroundColor: "rgba(255,255,255,0.03)",
          }} />
        ))}
      </div>

      {/* 타이틀 (오른쪽) */}
      <div style={{
        position: "absolute",
        right: 80,
        top: 0,
        bottom: 0,
        width: 1200,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}>
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 140,
          color: "#00ffff",
          textShadow: "0 0 30px #00ffff, 0 0 60px #00ffff80, 0 0 90px #00ffff40, 4px 4px 0 #003344",
          letterSpacing: 8,
          lineHeight: 1.3,
          textAlign: "center",
        }}>
          TETRIS
        </div>
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 56,
          color: "#ff6600",
          textShadow: "0 0 20px #ff6600, 0 0 40px #ff660080, 3px 3px 0 #331100",
          letterSpacing: 6,
          marginTop: 10,
        }}>
          Original
        </div>
        <div style={{
          width: 500,
          height: 3,
          background: "linear-gradient(90deg, transparent, #00ff41, transparent)",
          margin: "40px 0",
        }} />
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 52,
          color: "#00ff41",
          textShadow: "0 0 20px #00ff41, 0 0 40px #00ff4180, 3px 3px 0 #003300",
          letterSpacing: 10,
        }}>
          VIBE CODING
        </div>
      </div>

      {/* 스캔라인 */}
      <AbsoluteFill style={{
        background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px)",
        pointerEvents: "none",
      }} />
      {/* 비네트 */}
      <AbsoluteFill style={{
        background: "radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.5) 100%)",
        pointerEvents: "none",
      }} />
    </AbsoluteFill>
  );
};
