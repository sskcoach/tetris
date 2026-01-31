import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";

// 테트리스 보드 설정
const COLS = 10;
const ROWS = 20;
const CELL = 42;
const BOARD_W = COLS * CELL;
const BOARD_H = ROWS * CELL;

// 네온 컬러
const PIECE_COLORS: Record<string, string> = {
  I: "#00ffff",
  O: "#ffff00",
  T: "#cc00ff",
  S: "#00ff41",
  Z: "#ff3366",
  J: "#3366ff",
  L: "#ff6600",
};

// 미리 채워진 보드 (아래 4줄에 I-piece 빈칸 하나)
const generateBoard = (): (string | null)[][] => {
  const board: (string | null)[][] = Array.from({ length: ROWS }, () =>
    Array(COLS).fill(null)
  );

  const colors = Object.values(PIECE_COLORS);
  // 아래 4줄을 채움 (맨 왼쪽 열만 비워둠 — I-piece가 들어갈 자리)
  for (let r = ROWS - 4; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      if (c === 0) continue; // I-piece 자리
      board[r][c] = colors[(r * 3 + c * 7) % colors.length];
    }
  }
  // 그 위 2줄도 랜덤하게 채움 (불규칙하게)
  for (let r = ROWS - 6; r < ROWS - 4; r++) {
    for (let c = 0; c < COLS; c++) {
      if (Math.sin(r * 13 + c * 7) > -0.2) {
        board[r][c] = colors[(r * 5 + c * 3) % colors.length];
      }
    }
  }
  return board;
};

const BOARD = generateBoard();

const Cell: React.FC<{ color: string; x: number; y: number; glow?: boolean; opacity?: number }> = ({
  color,
  x,
  y,
  glow,
  opacity = 1,
}) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: CELL - 2,
      height: CELL - 2,
      backgroundColor: color,
      border: `1px solid ${color}88`,
      borderRadius: 3,
      opacity,
      boxShadow: glow
        ? `0 0 12px ${color}, 0 0 24px ${color}80`
        : `inset 1px 1px 0 ${color}44, inset -1px -1px 0 ${color}22`,
    }}
  />
);

export const SampleA_LineClear: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Phase 1: I-piece 떨어짐 (0~2초)
  const dropEnd = fps * 1.5;
  const iPieceTargetY = ROWS - 4; // row 16~19
  const iPieceStartY = -4;

  const iPieceY = interpolate(
    frame,
    [0, dropEnd * 0.7, dropEnd],
    [iPieceStartY, iPieceTargetY - 2, iPieceTargetY],
    { extrapolateRight: "clamp", easing: Easing.in(Easing.quad) }
  );

  // Phase 2: 착지 플래시 + 줄 클리어 (2~3.5초)
  const landed = frame >= dropEnd;
  const clearStart = dropEnd + fps * 0.3;
  const clearEnd = clearStart + fps * 0.6;
  const clearing = frame >= clearStart && frame < clearEnd;

  const clearFlash = landed
    ? interpolate(
        frame,
        [dropEnd, dropEnd + fps * 0.15, dropEnd + fps * 0.3],
        [0, 1, 0],
        { extrapolateRight: "clamp" }
      )
    : 0;

  // 클리어되는 줄의 투명도
  const clearOpacity = clearing
    ? interpolate(
        frame,
        [clearStart, clearEnd],
        [1, 0],
        { extrapolateRight: "clamp" }
      )
    : 1;

  // Phase 3: 텍스트 등장 (3.5~5초)
  const textStart = clearEnd;
  const textScale = interpolate(
    frame,
    [textStart, textStart + fps * 0.2, textStart + fps * 0.35],
    [0, 1.2, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
  );

  const textOpacity = interpolate(
    frame,
    [textStart, textStart + fps * 0.15],
    [0, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
  );

  // 텍스트 글로우 펄스
  const textGlow = interpolate(
    frame % (fps * 0.5),
    [0, fps * 0.25, fps * 0.5],
    [20, 40, 20]
  );

  const boardLeft = (1920 - BOARD_W) / 2;
  const boardTop = (1080 - BOARD_H) / 2;

  // 클리어된 줄인지 확인 (row 16~19)
  const isClearRow = (r: number) => r >= ROWS - 4;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a1a" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

      {/* 보드 배경 */}
      <div
        style={{
          position: "absolute",
          left: boardLeft - 4,
          top: boardTop - 4,
          width: BOARD_W + 8,
          height: BOARD_H + 8,
          border: "2px solid #333",
          borderRadius: 4,
          background: "rgba(0,0,0,0.6)",
        }}
      />

      {/* 보드 그리드 */}
      <div
        style={{
          position: "absolute",
          left: boardLeft,
          top: boardTop,
          width: BOARD_W,
          height: BOARD_H,
        }}
      >
        {/* 기존 블록 */}
        {BOARD.map((row, r) =>
          row.map((color, c) => {
            if (!color) return null;
            const isClearing = landed && isClearRow(r);
            return (
              <Cell
                key={`${r}-${c}`}
                color={color}
                x={c * CELL}
                y={r * CELL}
                opacity={isClearing ? clearOpacity : 1}
              />
            );
          })
        )}

        {/* 떨어지는 I-piece (세로) */}
        {!landed &&
          [0, 1, 2, 3].map((i) => (
            <Cell
              key={`i-${i}`}
              color={PIECE_COLORS.I}
              x={0}
              y={(iPieceY + i) * CELL}
              glow
            />
          ))}

        {/* 착지한 I-piece */}
        {landed &&
          [0, 1, 2, 3].map((i) => (
            <Cell
              key={`il-${i}`}
              color={PIECE_COLORS.I}
              x={0}
              y={(iPieceTargetY + i) * CELL}
              glow
              opacity={isClearRow(iPieceTargetY + i) ? clearOpacity : 1}
            />
          ))}
      </div>

      {/* 착지 플래시 */}
      {clearFlash > 0 && (
        <AbsoluteFill
          style={{
            backgroundColor: `rgba(255, 255, 255, ${clearFlash * 0.3})`,
          }}
        />
      )}

      {/* 클리어 시 줄 번쩍임 */}
      {clearing && (
        <>
          {[ROWS - 4, ROWS - 3, ROWS - 2, ROWS - 1].map((r) => (
            <div
              key={r}
              style={{
                position: "absolute",
                left: boardLeft,
                top: boardTop + r * CELL,
                width: BOARD_W,
                height: CELL,
                backgroundColor: `rgba(255, 255, 255, ${clearOpacity * 0.5})`,
                boxShadow: `0 0 30px rgba(255,255,255,${clearOpacity * 0.8})`,
              }}
            />
          ))}
        </>
      )}

      {/* TETRIS! 텍스트 */}
      {frame >= textStart && (
        <AbsoluteFill
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              transform: `scale(${textScale})`,
              opacity: textOpacity,
              textAlign: "center",
            }}
          >
            <div
              style={{
                fontFamily: "'Press Start 2P', monospace",
                fontSize: 120,
                color: "#00ffff",
                textShadow: `
                  0 0 ${textGlow}px #00ffff,
                  0 0 ${textGlow * 2}px #00ffff80,
                  0 0 ${textGlow * 3}px #00ffff40,
                  4px 4px 0 #000
                `,
                letterSpacing: 8,
                WebkitTextStroke: "2px #00cccc",
              }}
            >
              TETRIS!
            </div>
            <div
              style={{
                fontFamily: "'Press Start 2P', monospace",
                fontSize: 36,
                color: "#ffff00",
                textShadow: `0 0 15px #ffff00, 0 0 30px #ffff0080, 3px 3px 0 #000`,
                marginTop: 20,
                letterSpacing: 4,
              }}
            >
              바이브코딩으로 쓱 만드는
            </div>
          </div>
        </AbsoluteFill>
      )}

      {/* 비네트 */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.7) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* 스캔라인 */}
      <AbsoluteFill
        style={{
          background:
            "repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.06) 3px, rgba(0,0,0,0.06) 6px)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
