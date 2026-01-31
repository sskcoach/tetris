import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import "@fontsource/press-start-2p";
import "@fontsource/jetbrains-mono/700.css";

const COLORS = {
  I: "#00d4ff",
  O: "#ffd700",
  T: "#b44dff",
  S: "#00e676",
  Z: "#ff3d3d",
  J: "#3d7aff",
  L: "#ff8c00",
};

const TETRIMINOS: { piece: string; color: string }[] = [
  { piece: "[][][][]", color: COLORS.I },
  { piece: "[][]\n[][]", color: COLORS.O },
  { piece: " [] \n[][][]", color: COLORS.T },
  { piece: "[]\n[][][]", color: COLORS.J },
  { piece: "    []\n[][][]", color: COLORS.L },
  { piece: " [][]\n[][] ", color: COLORS.S },
  { piece: "[][] \n [][]\n", color: COLORS.Z },
];

// 떨어지는 T피스의 위치 (프레임별)
const FALLING_POSITIONS = [
  { row: 0, text: "      []        " },
  { row: 1, text: "    [][][]      " },
];

// 실제 게임 화면 ASCII (20행 보드)
const GAME_LINES = [
  "Score: 400 | Level: 1 | Lines: 7",
  "",
  "<! . . . . . . . . . . !>",
  "<! . . . . . . . . . . !>",
  "<! . . . . . . . . . . !>",
  "<! . . . .[][]. . . . .!>",
  "<! . . .[][]. . . . . .!>",
  "<! . . . . . . . . . . !>",
  "<! . . . . . . . . . . !>",
  "<! . . . . . . . . . . !>",
  "<! . . . . . . . . . . !>",
  "<! . . . . . . . . . . !>",
  "<! . . . . . . . . . . !>",
  "<! . . . . . . . . []. !>",
  "<! . . . . . . . [][]!>",
  "<! . . . . . . . .[][]!>",
  "<! . . . . . . . .[][]!>",
  "<! . . . .[]. .[][][][]!>",
  "<! . . . . .[]. .[][]!>",
  "<![][]. . .[]. .[][][]!>",
  "==========================",
  "  \\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/"
];

const NEXT_PIECE = [
  "NEXT",
  "|           |",
  "|  [][]     |",
  "|  [][]     |",
  "|           |",
];

export const Gif4_AsciiPlay: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // T피스 떨어지는 애니메이션 (0~끝 프레임에서 위에서 중간으로)
  const fallProgress = interpolate(frame, [0, durationInFrames - 1], [0, 5], {
    extrapolateRight: "clamp",
  });
  const fallRow = Math.floor(fallProgress);

  // 타이틀 펄스 (부드럽게)
  const pulse = interpolate(frame, [0, durationInFrames / 2, durationInFrames], [1, 1.01, 1]);
  
  // 글로우 애니메이션 (원본 복원)
  const glowIntensity = interpolate(frame, [0, durationInFrames / 2, durationInFrames], [0.5, 1, 0.5]);

  // 보드는 고정 (실제 게임 화면 그대로)

  return (
    <AbsoluteFill style={{ backgroundColor: "#080c24", overflow: "hidden" }}>
      {/* 폰트는 npm @fontsource로 로컬 로딩 */}

      {/* 배경 그라데이션 */}
      <AbsoluteFill style={{
        background: `
          radial-gradient(ellipse at 75% 50%, rgba(80,0,200,0.2) 0%, transparent 50%),
          radial-gradient(ellipse at 25% 40%, rgba(0,100,255,0.12) 0%, transparent 50%)
        `,
      }} />

      {/* 배경 아스키 테트리미노 (느리게 떠다님) */}
      {[
        { x: -20, y: 30, idx: 0, rot: 12, op: 0.07, speed: 0.3 },
        { x: 100, y: 580, idx: 1, rot: -8, op: 0.06, speed: -0.2 },
        { x: 1150, y: 20, idx: 4, rot: 20, op: 0.05, speed: 0.4 },
        { x: 1050, y: 620, idx: 3, rot: -15, op: 0.06, speed: -0.3 },
        { x: 500, y: 650, idx: 5, rot: 10, op: 0.05, speed: 0.2 },
        { x: 250, y: 450, idx: 2, rot: 5, op: 0.05, speed: -0.15 },
      ].map((b, i) => (
        <pre key={i} style={{
          position: "absolute",
          left: b.x,
          top: b.y + frame * b.speed,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: TETRIMINOS[b.idx].color,
          opacity: b.op,
          transform: `rotate(${b.rot + frame * 0.1}deg)`,
          whiteSpace: "pre",
          textShadow: `0 0 20px ${TETRIMINOS[b.idx].color}30`,
        }}>
          {TETRIMINOS[b.idx].piece}
        </pre>
      ))}

      {/* 왼쪽: 타이틀 영역 — 최상위 z-order */}
      <div style={{
        position: "absolute",
        left: 50,
        top: 50,
        width: 750,
        display: "flex",
        flexDirection: "column",
        zIndex: 100,
        transform: `scale(${pulse})`,
        transformOrigin: "left top",
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
          fontSize: 165,
          color: "#ffffff",
          textShadow: `
            0 0 ${40 * glowIntensity}px rgba(0,212,255,${0.5 * glowIntensity}),
            0 0 ${80 * glowIntensity}px rgba(0,212,255,${0.2 * glowIntensity}),
            5px 5px 0 #001a33
          `,
          letterSpacing: 10,
          lineHeight: 1.1,
        }}>
          TETRIS
        </div>

        {/* ORIGINAL */}
        <div style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 90,
          color: "#ff8c00",
          textShadow: `
            0 0 ${30 * glowIntensity}px rgba(255,140,0,${0.5 * glowIntensity}),
            0 0 ${60 * glowIntensity}px rgba(255,140,0,${0.2 * glowIntensity}),
            4px 4px 0 #331a00
          `,
          letterSpacing: 12,
          marginTop: 16,
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
          fontSize: 55,
          color: "#b44dff",
          textShadow: `
            0 0 ${25 * glowIntensity}px rgba(180,77,255,${0.4 * glowIntensity}),
            0 0 ${50 * glowIntensity}px rgba(180,77,255,${0.15 * glowIntensity}),
            3px 3px 0 #1a0033
          `,
          letterSpacing: 6,
        }}>
          VIBE CODING
        </div>
      </div>

      {/* 오른쪽: 실제 게임 화면 */}
      <div style={{
        position: "absolute",
        right: 40,
        top: 40,
        backgroundColor: "rgba(0,0,20,0.8)",
        borderRadius: 12,
        border: "2px solid rgba(0,212,255,0.2)",
        padding: "16px 20px",
        boxShadow: `
          0 0 40px rgba(0,212,255,0.15),
          inset 0 0 30px rgba(0,0,0,0.5)
        `,
        transform: "perspective(900px) rotateY(-6deg)",
        display: "flex",
        gap: 12,
      }}>
        {/* 보드 */}
        <div>
          {GAME_LINES.map((line, i) => (
            <pre key={i} style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: i === 0 ? 13 : 15,
              fontWeight: 700,
              lineHeight: 1.2,
              margin: 0,
              whiteSpace: "pre",
              color: i === 0 ? COLORS.I
                : i >= GAME_LINES.length - 2 ? "rgba(255,255,255,0.3)"
                : "rgba(255,255,255,0.5)",
            }}>
              {line.split(/(\[\])/).map((part, j) => 
                part === "[]" ? (
                  <span key={j} style={{
                    color: [COLORS.S, COLORS.T, COLORS.L, COLORS.J, COLORS.I, COLORS.Z, COLORS.O][j % 7],
                    textShadow: `0 0 6px ${[COLORS.S, COLORS.T, COLORS.L, COLORS.J, COLORS.I, COLORS.Z, COLORS.O][j % 7]}50`,
                  }}>{part}</span>
                ) : (
                  <span key={j} style={{
                    color: part.includes("<!") || part.includes("!>") || part.includes("==") || part.includes("\\/")
                      ? "rgba(255,255,255,0.25)"
                      : part.includes("Score") ? COLORS.I
                      : "rgba(255,255,255,0.15)",
                  }}>{part}</span>
                )
              )}
            </pre>
          ))}
        </div>

        {/* NEXT 피스 */}
        <div>
          {NEXT_PIECE.map((line, i) => (
            <pre key={i} style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 14,
              fontWeight: 700,
              lineHeight: 1.3,
              margin: 0,
              whiteSpace: "pre",
              color: i === 0 ? "rgba(255,255,255,0.4)" : "rgba(255,255,255,0.25)",
            }}>
              {line.split(/(\[\])/).map((part, j) =>
                part === "[]" ? (
                  <span key={j} style={{ color: COLORS.O, textShadow: `0 0 6px ${COLORS.O}50` }}>{part}</span>
                ) : (
                  <span key={j}>{part}</span>
                )
              )}
            </pre>
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
        boxShadow: `0 0 ${20 * glowIntensity}px rgba(0,212,255,0.3)`,
      }} />
    </AbsoluteFill>
  );
};
