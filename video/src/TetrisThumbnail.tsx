import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  staticFile,
} from "remotion";

// 테트리미노 색상 (네온)
const COLORS = [
  "#00ff41", // 초록
  "#00bfff", // 파랑
  "#ff00ff", // 핑크
  "#ffff00", // 노랑
  "#ff6600", // 주황
  "#00ffcc", // 시안
  "#ff3366", // 빨강
];

// 테트리미노 ASCII 모양들
const TETRIMINOS = [
  "[][][][] ", // I
  "[][]\n[][]", // O
  " []\n[][][]", // T
  "[]\n[][][]", // J
  "    []\n[][][]", // L
  " [][]\n[][] ", // S
  "[][] \n [][]\n", // Z
];

// 떨어지는 테트리미노 비 컬럼 생성
const generateRainColumns = (count: number) => {
  const columns: Array<{
    x: number;
    speed: number;
    offset: number;
    color: string;
    piece: string;
    opacity: number;
    size: number;
  }> = [];

  for (let i = 0; i < count; i++) {
    const seed = i * 7919 + 31;
    columns.push({
      x: ((seed * 13) % 1920),
      speed: 4.5 + ((seed * 17) % 100) / 17,
      offset: ((seed * 23) % 1000),
      color: COLORS[(seed * 3) % COLORS.length],
      piece: TETRIMINOS[(seed * 11) % TETRIMINOS.length],
      opacity: 0.15 + ((seed * 29) % 100) / 200,
      size: [60, 120, 200][(seed * 37) % 3],
    });
  }
  return columns;
};

const rainColumns = generateRainColumns(60);

const FallingPiece: React.FC<{
  x: number;
  speed: number;
  offset: number;
  color: string;
  piece: string;
  opacity: number;
  size: number;
  frame: number;
}> = ({ x, speed, offset, color, piece, opacity, size, frame }) => {
  const totalHeight = 1080 + 200;
  const y = ((frame * speed + offset) % totalHeight) - 100;

  return (
    <pre
      style={{
        position: "absolute",
        left: x,
        top: y,
        color,
        opacity,
        fontSize: size,
        fontFamily: "'Courier New', monospace",
        fontWeight: "bold",
        lineHeight: 1.1,
        textShadow: `0 0 8px ${color}40`,
        whiteSpace: "pre",
        margin: 0,
      }}
    >
      {piece}
    </pre>
  );
};

const fontUrl = "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap";

export const TetrisThumbnail: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 심장박동 펄스 (빠르게 커졌다 작아졌다)
  const heartbeat = interpolate(
    frame % (fps * 0.8),
    [0, fps * 0.1, fps * 0.2, fps * 0.35, fps * 0.45, fps * 0.8],
    [1, 1.12, 1, 1.08, 1, 1],
    { extrapolateRight: "clamp" }
  );

  // 글로우 펄스
  const glowIntensity = interpolate(
    frame % (fps * 0.8),
    [0, fps * 0.1, fps * 0.2, fps * 0.35, fps * 0.45, fps * 0.8],
    [15, 35, 15, 28, 15, 15],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a1a",
        overflow: "hidden",
      }}
    >
      {/* 레트로 폰트 로드 */}
      <style>{`@import url('${fontUrl}');`}</style>
      {/* 배경 그라데이션 오버레이 */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(0,50,80,0.3) 0%, transparent 70%)",
        }}
      />

      {/* 떨어지는 테트리미노 비 */}
      {rainColumns.map((col, i) => (
        <FallingPiece key={i} {...col} frame={frame} />
      ))}

      {/* 스캔라인 효과 */}
      <AbsoluteFill
        style={{
          background:
            "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.08) 2px, rgba(0,0,0,0.08) 4px)",
          pointerEvents: "none",
        }}
      />

      {/* 중앙 다크 패널 */}
      <AbsoluteFill
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            background: "rgba(5, 5, 20, 0.7)",
            border: "2px solid rgba(0, 255, 65, 0.4)",
            borderRadius: 8,
            padding: "50px 80px",
            boxShadow: `0 0 40px rgba(0, 255, 65, 0.15), inset 0 0 60px rgba(0, 0, 0, 0.5)`,
          }}
        >
          {/* 타이틀 */}
          <div
            style={{
              transform: `scale(${heartbeat})`,
              textAlign: "center",
            }}
          >
            <div
              style={{
                fontFamily: "'Press Start 2P', 'Courier New', monospace",
                fontWeight: 900,
                fontSize: 100,
                color: "#00ff41",
                textShadow: `
                  0 0 ${glowIntensity}px #00ff41,
                  0 0 ${glowIntensity * 2}px #00ff4180,
                  0 0 ${glowIntensity * 3}px #00ff4140
                `,
                letterSpacing: 6,
                lineHeight: 1.2,
              }}
            >
              TETRIS ORIGINAL
            </div>
            <div
              style={{
                fontFamily: "'Press Start 2P', 'Courier New', monospace",
                fontWeight: 700,
                fontSize: 68,
                color: "#ffff00",
                textShadow: `
                  0 0 ${glowIntensity}px #ffff00,
                  0 0 ${glowIntensity * 2}px #ffff0080
                `,
                letterSpacing: 4,
                marginTop: 10,
              }}
            >
              with VIBE CODING
            </div>
          </div>
        </div>
      </AbsoluteFill>

      {/* 비네트 효과 */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.6) 100%)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
