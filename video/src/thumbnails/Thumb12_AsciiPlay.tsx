import React from "react";
import { AbsoluteFill } from "remotion";

// 테트리스 블록 색상
const COLORS = {
  I: "#00d4ff",
  O: "#ffd700",
  T: "#b44dff",
  S: "#00e676",
  Z: "#ff3d3d",
  J: "#3d7aff",
  L: "#ff8c00",
};

// 아스키 테트리미노 (오리지널 스타일)
const TETRIMINOS: { piece: string; color: string }[] = [
  { piece: "[][][][]", color: COLORS.I },
  { piece: "[][]\n[][]", color: COLORS.O },
  { piece: " [] \n[][][]", color: COLORS.T },
  { piece: "[]\n[][][]", color: COLORS.J },
  { piece: "    []\n[][][]", color: COLORS.L },
  { piece: " [][]\n[][] ", color: COLORS.S },
  { piece: "[][] \n [][]\n", color: COLORS.Z },
];

// 아스키 보드 - 실제 게임 화면처럼
const BOARD_ASCII = [
  "                    ",
  "                    ",
  "        []          ",
  "      [][][]        ",
  "                    ",
  "                    ",
  "                []  ",
  "[]            [][]  ",
  "[][]    [][]  [][]  ",
  "[][]  [][][][][][][]",
  "[][][][][][][][][]  ",
  "[][][][][][][][][][]",
];

// 보드 셀 색상 매핑 (행, 시작열)
const BOARD_COLORS: { row: number; col: number; len: number; color: string }[] = [
  { row: 2, col: 8, len: 2, color: COLORS.T },
  { row: 3, col: 6, len: 8, color: COLORS.T },
  { row: 6, col: 16, len: 2, color: COLORS.L },
  { row: 7, col: 0, len: 2, color: COLORS.S },
  { row: 7, col: 14, len: 4, color: COLORS.L },
  { row: 8, col: 0, len: 4, color: COLORS.S },
  { row: 8, col: 8, len: 4, color: COLORS.O },
  { row: 8, col: 14, len: 2, color: COLORS.L },
  { row: 8, col: 16, len: 4, color: COLORS.J },
  { row: 9, col: 0, len: 4, color: COLORS.Z },
  { row: 9, col: 6, len: 14, color: COLORS.I },
  { row: 10, col: 0, len: 18, color: COLORS.T },
  { row: 11, col: 0, len: 20, color: COLORS.S },
];

export const Thumb12_AsciiPlay: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#080c24", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@800;900&family=JetBrains+Mono:wght@700&display=swap');`}</style>

      {/* 배경 그라데이션 */}
      <AbsoluteFill style={{
        background: `
          radial-gradient(ellipse at 75% 50%, rgba(80,0,200,0.2) 0%, transparent 50%),
          radial-gradient(ellipse at 25% 40%, rgba(0,100,255,0.12) 0%, transparent 50%)
        `,
      }} />

      {/* 배경 아스키 테트리미노 흩뿌리기 */}
      {[
        { x: -20, y: 30, idx: 0, rot: 12, op: 0.07 },
        { x: 100, y: 580, idx: 1, rot: -8, op: 0.06 },
        { x: 1150, y: 20, idx: 4, rot: 20, op: 0.05 },
        { x: 1050, y: 620, idx: 3, rot: -15, op: 0.06 },
        { x: 500, y: 650, idx: 5, rot: 10, op: 0.05 },
        { x: 1300, y: 300, idx: 6, rot: -25, op: 0.04 },
        { x: 250, y: 450, idx: 2, rot: 5, op: 0.05 },
      ].map((b, i) => (
        <pre key={i} style={{
          position: "absolute",
          left: b.x,
          top: b.y,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: TETRIMINOS[b.idx].color,
          opacity: b.op,
          transform: `rotate(${b.rot}deg)`,
          whiteSpace: "pre",
          textShadow: `0 0 20px ${TETRIMINOS[b.idx].color}30`,
        }}>
          {TETRIMINOS[b.idx].piece}
        </pre>
      ))}

      {/* 왼쪽: 타이틀 영역 — 최상위 z-order */}
      <div style={{
        position: "absolute",
        left: 70,
        top: 80,
        width: 550,
        display: "flex",
        flexDirection: "column",
        zIndex: 100,
      }}>
        {/* 배지 */}
        <div style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
          backgroundColor: "rgba(0,212,255,0.12)",
          border: "1px solid rgba(0,212,255,0.25)",
          borderRadius: 20,
          padding: "8px 18px",
          marginBottom: 28,
          width: "fit-content",
        }}>
          <span style={{ fontSize: 16 }}>🤖</span>
          <span style={{
            fontFamily: "'Inter', sans-serif",
            fontSize: 15,
            fontWeight: 800,
            color: "#00d4ff",
            letterSpacing: 1.5,
          }}>MADE WITH AI</span>
        </div>

        {/* TETRIS */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 115,
          color: "#ffffff",
          textShadow: `
            0 0 30px rgba(0,212,255,0.5),
            0 0 60px rgba(0,212,255,0.2),
            4px 4px 0 #001a33
          `,
          letterSpacing: 8,
          lineHeight: 1.1,
        }}>
          TETRIS
        </div>

        {/* ORIGINAL */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 68,
          color: "#ff8c00",
          textShadow: `
            0 0 25px rgba(255,140,0,0.5),
            0 0 50px rgba(255,140,0,0.2),
            3px 3px 0 #331a00
          `,
          letterSpacing: 10,
          marginTop: 12,
        }}>
          ORIGINAL
        </div>

        {/* 아스키 블록 구분선 */}
        <pre style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 18,
          fontWeight: 700,
          margin: "20px 0",
          whiteSpace: "pre",
          lineHeight: 1,
        }}>
          <span style={{ color: COLORS.I, textShadow: `0 0 10px ${COLORS.I}60` }}>[]</span>
          <span style={{ color: COLORS.O, textShadow: `0 0 10px ${COLORS.O}60` }}>[]</span>
          <span style={{ color: COLORS.T, textShadow: `0 0 10px ${COLORS.T}60` }}>[]</span>
          <span style={{ color: COLORS.S, textShadow: `0 0 10px ${COLORS.S}60` }}>[]</span>
          <span style={{ color: COLORS.Z, textShadow: `0 0 10px ${COLORS.Z}60` }}>[]</span>
          <span style={{ color: COLORS.J, textShadow: `0 0 10px ${COLORS.J}60` }}>[]</span>
          <span style={{ color: COLORS.L, textShadow: `0 0 10px ${COLORS.L}60` }}>[]</span>
        </pre>

        {/* VIBE CODING */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 42,
          color: "#b44dff",
          textShadow: `
            0 0 20px rgba(180,77,255,0.4),
            0 0 40px rgba(180,77,255,0.15),
            2px 2px 0 #1a0033
          `,
          letterSpacing: 5,
        }}>
          VIBE CODING
        </div>
      </div>

      {/* 오른쪽: 아스키 테트리스 보드 */}
      <div style={{
        position: "absolute",
        right: 80,
        top: 60,
        backgroundColor: "rgba(0,0,20,0.75)",
        borderRadius: 12,
        border: "2px solid rgba(0,212,255,0.2)",
        padding: "20px 24px",
        boxShadow: `
          0 0 40px rgba(0,212,255,0.15),
          inset 0 0 30px rgba(0,0,0,0.5)
        `,
        transform: "perspective(900px) rotateY(-6deg)",
      }}>
        {/* 보드 헤더 */}
        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 14,
          fontWeight: 700,
          color: "rgba(255,255,255,0.3)",
          marginBottom: 12,
          letterSpacing: 2,
        }}>
          ╔══════════════════════╗
        </div>

        {/* 보드 내용 */}
        {BOARD_ASCII.map((row, ry) => (
          <pre key={ry} style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 28,
            fontWeight: 700,
            lineHeight: 1.15,
            margin: 0,
            whiteSpace: "pre",
            letterSpacing: 0,
          }}>
            {/* 각 행 렌더링 - 색상 적용 */}
            {row.split("").map((char, cx) => {
              // 이 위치에 해당하는 색상 찾기
              const colorInfo = BOARD_COLORS.find(
                (c) => c.row === ry && cx >= c.col && cx < c.col + c.len
              );
              const color = colorInfo
                ? colorInfo.color
                : char !== " "
                ? "rgba(255,255,255,0.15)"
                : "transparent";
              return (
                <span key={cx} style={{
                  color: color,
                  textShadow: colorInfo ? `0 0 8px ${color}50` : "none",
                }}>
                  {char}
                </span>
              );
            })}
          </pre>
        ))}

        {/* 보드 푸터 */}
        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 14,
          fontWeight: 700,
          color: "rgba(255,255,255,0.3)",
          marginTop: 12,
          letterSpacing: 2,
        }}>
          ╚══════════════════════╝
        </div>
      </div>

      {/* NEXT 미리보기 */}
      <pre style={{
        position: "absolute",
        right: 40,
        top: 80,
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 14,
        fontWeight: 700,
        color: "rgba(255,255,255,0.25)",
        whiteSpace: "pre",
      }}>
        {`NEXT\n`}
        <span style={{ color: COLORS.I, fontSize: 18, textShadow: `0 0 8px ${COLORS.I}40` }}>{"[][][][]"}</span>
      </pre>

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
