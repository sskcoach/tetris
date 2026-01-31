import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";

// 테트리미노 모양 + 색상
const PIECES = [
  { shape: [[1,1,1,1]], color: "#00ffff" },           // I
  { shape: [[1,1],[1,1]], color: "#ffff00" },          // O
  { shape: [[0,1,0],[1,1,1]], color: "#cc00ff" },      // T
  { shape: [[1,0],[1,0],[1,1]], color: "#ff6600" },     // L
  { shape: [[0,1],[0,1],[1,1]], color: "#3366ff" },     // J
  { shape: [[0,1,1],[1,1,0]], color: "#00ff41" },       // S
  { shape: [[1,1,0],[0,1,1]], color: "#ff3366" },       // Z
];

const CELL = 36;

const TerminalPrompt: React.FC<{ text: string; charCount: number; showCursor: boolean }> = ({
  text,
  charCount,
  showCursor,
}) => {
  const displayed = text.slice(0, Math.floor(charCount));
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 0 }}>
      <span style={{ color: "#00ff41" }}>❯ </span>
      <span style={{ color: "#e0e0e0" }}>{displayed}</span>
      {showCursor && (
        <span
          style={{
            display: "inline-block",
            width: 14,
            height: 28,
            backgroundColor: "#00ff41",
            marginLeft: 2,
            opacity: 0.9,
          }}
        />
      )}
    </div>
  );
};

// 폭발적으로 등장하는 블록
const ExplodingPiece: React.FC<{
  piece: typeof PIECES[0];
  startFrame: number;
  targetX: number;
  targetY: number;
  frame: number;
  fps: number;
  index: number;
}> = ({ piece, startFrame, targetX, targetY, frame, fps, index }) => {
  const elapsed = frame - startFrame;
  if (elapsed < 0) return null;

  const duration = fps * 0.4;
  const progress = Math.min(elapsed / duration, 1);
  const eased = Easing.out(Easing.back(1.5))(progress);

  // 각 블록의 시작 위치 (화면 중앙에서 방사형으로)
  const angle = (index * 137.5 * Math.PI) / 180; // 황금각
  const startX = 960 + Math.cos(angle) * 800;
  const startY = 540 + Math.sin(angle) * 600;

  const x = startX + (targetX - startX) * eased;
  const y = startY + (targetY - startY) * eased;

  const scale = interpolate(progress, [0, 0.5, 1], [0.3, 1.2, 1]);
  const opacity = interpolate(progress, [0, 0.2], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `scale(${scale})`,
        opacity,
      }}
    >
      {piece.shape.map((row, r) =>
        row.map((cell, c) =>
          cell ? (
            <div
              key={`${r}-${c}`}
              style={{
                position: "absolute",
                left: c * CELL,
                top: r * CELL,
                width: CELL - 2,
                height: CELL - 2,
                backgroundColor: piece.color,
                border: `1px solid ${piece.color}88`,
                borderRadius: 3,
                boxShadow: `0 0 10px ${piece.color}80`,
              }}
            />
          ) : null
        )
      )}
    </div>
  );
};

export const SampleB_AITyping: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Phase 1: 타이핑 (0~2초)
  const typingText = "테트리스 만들어줘";
  const charsPerSec = 8;
  const charCount = Math.min(frame * charsPerSec / fps, typingText.length);
  const typingDone = charCount >= typingText.length;
  const cursorBlink = Math.floor(frame / (fps * 0.4)) % 2 === 0;

  // Phase 2: 블록 폭발 (2~3.5초)
  const explodeStart = fps * 2;

  // 블록 배치 위치 (화면 하단 중앙에 랜덤 배치)
  const blockPositions = PIECES.map((_, i) => ({
    x: 500 + (i % 4) * 250 + ((i * 73) % 80),
    y: 450 + Math.floor(i / 4) * 200 + ((i * 47) % 60),
    delay: i * 3,
  }));

  // Phase 3: 타이틀 (3.5~5초)
  const titleStart = fps * 3.2;
  const titleOpacity = interpolate(
    frame,
    [titleStart, titleStart + fps * 0.3],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const titleY = interpolate(
    frame,
    [titleStart, titleStart + fps * 0.4],
    [40, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) }
  );

  // 배경 그라데이션 변화
  const bgBrightness = interpolate(
    frame,
    [explodeStart, explodeStart + fps * 0.5],
    [0, 0.15],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d1117" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>

      {/* 배경 글로우 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at center, rgba(0,255,65,${bgBrightness}) 0%, transparent 60%)`,
        }}
      />

      {/* 터미널 윈도우 */}
      <div
        style={{
          position: "absolute",
          left: 460,
          top: 180,
          width: 1000,
          height: 160,
          background: "rgba(13, 17, 23, 0.95)",
          border: "1px solid #333",
          borderRadius: 12,
          overflow: "hidden",
          boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
        }}
      >
        {/* 터미널 상단바 */}
        <div
          style={{
            height: 36,
            background: "#1c2130",
            display: "flex",
            alignItems: "center",
            padding: "0 14px",
            gap: 8,
          }}
        >
          <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#ff5f57" }} />
          <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#febc2e" }} />
          <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#28c840" }} />
          <span style={{ color: "#666", marginLeft: 12, fontSize: 14, fontFamily: "monospace" }}>
            gemini
          </span>
        </div>

        {/* 터미널 내용 */}
        <div
          style={{
            padding: "16px 20px",
            fontFamily: "'Fira Code', 'SF Mono', monospace",
            fontSize: 28,
            lineHeight: 1.6,
          }}
        >
          <TerminalPrompt
            text={typingText}
            charCount={charCount}
            showCursor={!typingDone || cursorBlink}
          />
        </div>
      </div>

      {/* 폭발 블록들 */}
      {frame >= explodeStart &&
        PIECES.map((piece, i) => (
          <ExplodingPiece
            key={i}
            piece={piece}
            startFrame={explodeStart + blockPositions[i].delay}
            targetX={blockPositions[i].x}
            targetY={blockPositions[i].y}
            frame={frame}
            fps={fps}
            index={i}
          />
        ))}

      {/* 타이틀 */}
      {frame >= titleStart && (
        <div
          style={{
            position: "absolute",
            bottom: 100,
            width: "100%",
            textAlign: "center",
            opacity: titleOpacity,
            transform: `translateY(${titleY}px)`,
          }}
        >
          <div
            style={{
              fontFamily: "'Press Start 2P', monospace",
              fontSize: 64,
              color: "#00ff41",
              textShadow: "0 0 20px #00ff41, 0 0 40px #00ff4180, 3px 3px 0 #000",
              letterSpacing: 4,
            }}
          >
            AI한테 시켜서 만든
          </div>
          <div
            style={{
              fontFamily: "'Press Start 2P', monospace",
              fontSize: 80,
              color: "#00ffff",
              textShadow: "0 0 25px #00ffff, 0 0 50px #00ffff80, 3px 3px 0 #000",
              marginTop: 16,
              letterSpacing: 6,
            }}
          >
            TETRIS
          </div>
        </div>
      )}

      {/* 스캔라인 */}
      <AbsoluteFill
        style={{
          background:
            "repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.05) 3px, rgba(0,0,0,0.05) 6px)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
