import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";

const CELL = 48;

// "TETRIS" 를 테트리미노 블록으로 표현 (6x5 그리드 per letter, 간소화)
const BLOCK_LETTERS: Record<string, number[][]> = {
  T: [
    [1, 1, 1],
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
  ],
  E: [
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 0],
    [1, 1, 1],
  ],
  R: [
    [1, 1, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 0, 1],
  ],
  I: [
    [1, 1, 1],
    [0, 1, 0],
    [0, 1, 0],
    [1, 1, 1],
  ],
  S: [
    [0, 1, 1],
    [1, 0, 0],
    [0, 1, 0],
    [1, 1, 0],
  ],
};

const LETTER_ORDER = ["T", "E", "T", "R", "I", "S"];

const LETTER_COLORS = [
  "#00ffff", // T - 시안
  "#ff3366", // E - 핑크
  "#ffff00", // T - 노랑
  "#00ff41", // R - 초록
  "#ff6600", // I - 주황
  "#cc00ff", // S - 보라
];

// 각 블록이 위에서 떨어져서 제자리를 찾는 애니메이션
const FallingBlock: React.FC<{
  x: number;
  y: number;
  color: string;
  startFrame: number;
  frame: number;
  fps: number;
  finalGlow: boolean;
}> = ({ x, y, color, startFrame, frame, fps, finalGlow }) => {
  const elapsed = frame - startFrame;
  if (elapsed < 0) return null;

  const dropDuration = fps * 0.35;
  const progress = Math.min(elapsed / dropDuration, 1);
  const eased = Easing.bezier(0.34, 1.56, 0.64, 1)(progress);

  const startY = -100 - Math.random() * 200;
  const currentY = startY + (y - startY) * eased;
  const opacity = interpolate(progress, [0, 0.3], [0, 1], { extrapolateRight: "clamp" });

  // 착지 바운스
  const bounce = progress >= 0.8
    ? Math.sin((progress - 0.8) * 5 * Math.PI) * 3 * (1 - progress)
    : 0;

  const glowSize = finalGlow ? 12 : 6;

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: currentY + bounce,
        width: CELL - 3,
        height: CELL - 3,
        backgroundColor: color,
        border: `1px solid ${color}aa`,
        borderRadius: 4,
        opacity,
        boxShadow: finalGlow
          ? `0 0 ${glowSize}px ${color}, 0 0 ${glowSize * 2}px ${color}60`
          : `inset 2px 2px 0 ${color}44, inset -2px -2px 0 ${color}22`,
      }}
    />
  );
};

export const SampleC_RetroGlow: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 전체 블록 데이터 생성
  const allBlocks: Array<{
    x: number;
    y: number;
    color: string;
    delay: number;
  }> = [];

  const totalWidth =
    LETTER_ORDER.length * 3 * CELL + (LETTER_ORDER.length - 1) * CELL;
  const startX = (1920 - totalWidth) / 2;
  const startY = 240;

  let blockIndex = 0;
  LETTER_ORDER.forEach((letter, li) => {
    const grid = BLOCK_LETTERS[letter];
    const color = LETTER_COLORS[li];
    const letterX = startX + li * (3 * CELL + CELL);

    grid.forEach((row, r) => {
      row.forEach((cell, c) => {
        if (cell) {
          allBlocks.push({
            x: letterX + c * CELL,
            y: startY + r * CELL,
            color,
            delay: li * 6 + blockIndex * 0.8,
          });
          blockIndex++;
        }
      });
    });
  });

  // Phase 1: 블록 떨어짐 (0~3초)
  const dropPhaseStart = fps * 0.3;

  // Phase 2: 완성 후 글로우 (3~3.5초)
  const allLanded = fps * 3;
  const glowActive = frame >= allLanded;

  // 글로우 펄스
  const glowPulse = glowActive
    ? interpolate(
        (frame - allLanded) % (fps * 0.6),
        [0, fps * 0.3, fps * 0.6],
        [1, 1.5, 1]
      )
    : 1;

  // Phase 3: 서브타이틀 (3.5~5초)
  const subStart = fps * 3.3;
  const subOpacity = interpolate(
    frame,
    [subStart, subStart + fps * 0.4],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const subY = interpolate(
    frame,
    [subStart, subStart + fps * 0.5],
    [30, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) }
  );

  // 배경 파티클 (미세한 점들)
  const particles = Array.from({ length: 30 }, (_, i) => {
    const seed = i * 7919;
    const px = (seed * 13) % 1920;
    const speed = 0.5 + ((seed * 17) % 100) / 100;
    const py = ((frame * speed + (seed * 23) % 1000) % 1200) - 60;
    const size = 2 + ((seed * 29) % 3);
    const pOpacity = 0.1 + ((seed * 31) % 100) / 500;
    return { px, py, size, pOpacity };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a1a" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

      {/* 배경 그라데이션 */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at 50% 40%, rgba(0,50,100,0.2) 0%, transparent 60%)",
        }}
      />

      {/* 배경 파티클 */}
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: p.px,
            top: p.py,
            width: p.size,
            height: p.size,
            borderRadius: "50%",
            backgroundColor: "#ffffff",
            opacity: p.pOpacity,
          }}
        />
      ))}

      {/* 떨어지는 블록 글자들 */}
      <div style={{ transform: `scale(${glowPulse})`, transformOrigin: "50% 35%" }}>
        {allBlocks.map((block, i) => (
          <FallingBlock
            key={i}
            x={block.x}
            y={block.y}
            color={block.color}
            startFrame={dropPhaseStart + block.delay}
            frame={frame}
            fps={fps}
            finalGlow={glowActive}
          />
        ))}
      </div>

      {/* 서브타이틀 */}
      {frame >= subStart && (
        <div
          style={{
            position: "absolute",
            bottom: 200,
            width: "100%",
            textAlign: "center",
            opacity: subOpacity,
            transform: `translateY(${subY}px)`,
          }}
        >
          <div
            style={{
              fontFamily: "'Press Start 2P', monospace",
              fontSize: 44,
              color: "#ffffff",
              textShadow: "0 0 15px rgba(255,255,255,0.5), 3px 3px 0 #000",
              letterSpacing: 3,
            }}
          >
            바이브코딩으로 쓱 만드는
          </div>
          <div
            style={{
              fontFamily: "'Press Start 2P', monospace",
              fontSize: 28,
              color: "#888",
              marginTop: 16,
              letterSpacing: 6,
            }}
          >
            VIBE CODING × GEMINI CLI
          </div>
        </div>
      )}

      {/* 비네트 */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.6) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* 스캔라인 */}
      <AbsoluteFill
        style={{
          background:
            "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.04) 2px, rgba(0,0,0,0.04) 4px)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
