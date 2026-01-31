import React from "react";
import { AbsoluteFill } from "remotion";

// 아케이드 레트로 스타일 — CRT 모니터 느낌
export const Thumb4_RetroArcade: React.FC = () => {
  // 큰 블록 글자로 TETRIS
  const CELL = 36;
  const BLOCK_LETTERS: Record<string, number[][]> = {
    T: [[1,1,1],[0,1,0],[0,1,0],[0,1,0]],
    E: [[1,1,1],[1,0,0],[1,1,0],[1,1,1]],
    R: [[1,1,0],[1,0,1],[1,1,0],[1,0,1]],
    I: [[1,1,1],[0,1,0],[0,1,0],[1,1,1]],
    S: [[0,1,1],[1,0,0],[0,1,0],[1,1,0]],
  };
  const letters = [
    { ch: "T", color: "#00ffff" },
    { ch: "E", color: "#ff3366" },
    { ch: "T", color: "#ffff00" },
    { ch: "R", color: "#00ff41" },
    { ch: "I", color: "#ff6600" },
    { ch: "S", color: "#cc00ff" },
  ];

  const totalW = letters.length * 3 * CELL + (letters.length - 1) * CELL * 0.5;
  const startX = (1920 - totalW) / 2;
  const startY = 200;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0014", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

      {/* 방사형 보라 배경 */}
      <AbsoluteFill style={{
        background: `
          radial-gradient(ellipse at 50% 40%, rgba(80,0,120,0.4) 0%, transparent 60%),
          radial-gradient(ellipse at 20% 80%, rgba(0,50,100,0.3) 0%, transparent 40%),
          radial-gradient(ellipse at 80% 20%, rgba(100,0,50,0.2) 0%, transparent 40%)
        `,
      }} />

      {/* 격자 바닥 (퍼스펙티브) */}
      <div style={{
        position: "absolute", bottom: 0, left: 0, right: 0, height: 400,
        background: `
          repeating-linear-gradient(90deg, rgba(0,255,255,0.08) 0px, transparent 1px, transparent 80px),
          repeating-linear-gradient(0deg, rgba(0,255,255,0.06) 0px, transparent 1px, transparent 40px)
        `,
        transform: "perspective(600px) rotateX(60deg)",
        transformOrigin: "bottom center",
      }} />

      {/* 블록 글자 TETRIS */}
      {letters.map((letter, li) => {
        const grid = BLOCK_LETTERS[letter.ch];
        const lx = startX + li * (3 * CELL + CELL * 0.5);
        return grid.map((row, r) =>
          row.map((cell, c) => cell ? (
            <div key={`${li}-${r}-${c}`} style={{
              position: "absolute",
              left: lx + c * CELL,
              top: startY + r * CELL,
              width: CELL - 3, height: CELL - 3,
              backgroundColor: letter.color,
              border: `1px solid ${letter.color}aa`,
              borderRadius: 4,
              boxShadow: `0 0 12px ${letter.color}, 0 0 24px ${letter.color}60`,
            }} />
          ) : null)
        );
      })}

      {/* Original 서브타이틀 */}
      <div style={{
        position: "absolute",
        top: startY + 4 * CELL + 40,
        width: "100%",
        textAlign: "center",
      }}>
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 60,
          color: "#ff6600",
          textShadow: "0 0 20px #ff6600, 0 0 40px #ff660080, 3px 3px 0 #331100",
          letterSpacing: 8,
        }}>
          Original
        </div>
      </div>

      {/* 하단 VIBE CODING */}
      <div style={{
        position: "absolute",
        bottom: 120,
        width: "100%",
        textAlign: "center",
      }}>
        <div style={{
          display: "inline-block",
          background: "rgba(0,0,0,0.6)",
          border: "1px solid #00ff4166",
          borderRadius: 8,
          padding: "20px 60px",
        }}>
          <span style={{
            fontFamily: "'Press Start 2P', monospace",
            fontSize: 48,
            color: "#00ff41",
            textShadow: "0 0 20px #00ff41, 0 0 40px #00ff4180",
            letterSpacing: 12,
          }}>
            VIBE CODING
          </span>
        </div>
      </div>

      {/* CRT 스캔라인 */}
      <AbsoluteFill style={{
        background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)",
        pointerEvents: "none",
      }} />
      {/* CRT 비네트 */}
      <AbsoluteFill style={{
        background: "radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.7) 100%)",
        pointerEvents: "none",
      }} />
      {/* CRT 곡면 반사 */}
      <AbsoluteFill style={{
        background: "linear-gradient(135deg, rgba(255,255,255,0.03) 0%, transparent 50%)",
        pointerEvents: "none",
      }} />
    </AbsoluteFill>
  );
};
