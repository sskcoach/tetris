import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";

// 기본: 비 내림 + 타이틀 펄스
const TETRIMINO_ASCII = [
  "[][][][]", "[][]\n[][]", " []\n[][][]", "[]\n[][][]",
  "    []\n[][][]", " [][]\n[][]", "[][]\n [][]",
];

const colors = ["#00ff41", "#00cc33", "#00ff66", "#33ff77", "#00dd44", "#00ffcc", "#22ee55", "#44ff88"];

const generateRain = (count: number, seed0: number, canvasW: number) => {
  const items: Array<{ x: number; speed: number; offset: number; piece: string; opacity: number; size: number; color: string }> = [];
  const colWidth = canvasW / count;
  for (let i = 0; i < count; i++) {
    const s = i * 7919 + seed0;
    const jitter = ((s * 37) % Math.floor(colWidth * 0.7)) - colWidth * 0.35;
    items.push({
      x: Math.floor(i * colWidth + colWidth * 0.5 + jitter),
      speed: 6.0 + ((s * 17) % 100) / 10,
      offset: ((s * 23) % 1000),
      piece: TETRIMINO_ASCII[(s * 11) % TETRIMINO_ASCII.length],
      opacity: 0.4 + ((s * 29) % 100) / 200,
      size: 28 + ((s * 7) % 22),
      color: colors[(s * 3) % colors.length],
    });
  }
  return items;
};

// 1080x720 기준
const rain = generateRain(60, 31, 1080);
const bright = generateRain(18, 67, 1080).map(r => ({ ...r, opacity: Math.min(r.opacity * 1.8, 0.9), speed: r.speed * 0.8 }));

export const Gif1_RainPulse: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, height: H } = useVideoConfig();

  const loopH = H + 200;

  // 펄스 — 심장박동 (시작부터 큰 상태)
  const pulse = interpolate(
    frame % (fps * 0.8),
    [0, fps * 0.1, fps * 0.2, fps * 0.4, fps * 0.5, fps * 0.8],
    [1.02, 1.02, 1, 1.02, 1, 1.02],
    { extrapolateRight: "clamp" }
  );

  const glow = interpolate(
    frame % (fps * 0.8),
    [0, fps * 0.1, fps * 0.2, fps * 0.4, fps * 0.5, fps * 0.8],
    [20, 40, 20, 32, 20, 20],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#020a02", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, rgba(0,60,0,0.5) 0%, transparent 55%)" }} />

      {/* 비 내리는 배경 */}
      {rain.map((r, i) => {
        const y = ((frame * r.speed + r.offset) % loopH) - 150;
        return (
          <pre key={`r${i}`} style={{
            position: "absolute", left: r.x, top: y,
            color: r.color, opacity: r.opacity,
            fontSize: r.size, fontFamily: "'Courier New', monospace",
            fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
            textShadow: `0 0 10px ${r.color}70, 0 0 20px ${r.color}40`,
          }}>
            {r.piece}
          </pre>
        );
      })}
      {bright.map((r, i) => {
        const y = ((frame * r.speed + r.offset) % loopH) - 150;
        return (
          <pre key={`b${i}`} style={{
            position: "absolute", left: r.x, top: y,
            color: r.color, opacity: Math.min(r.opacity, 0.6),
            fontSize: r.size, fontFamily: "'Courier New', monospace",
            fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
            textShadow: `0 0 10px ${r.color}80, 0 0 20px ${r.color}40`,
          }}>
            {r.piece}
          </pre>
        );
      })}

      <AbsoluteFill style={{ background: "radial-gradient(ellipse 65% 50% at 50% 48%, rgba(0,0,0,0.55) 0%, transparent 100%)", pointerEvents: "none" }} />

      {/* 타이틀 — 60~65% 영역 */}
      <AbsoluteFill style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 24 }}>
        <div style={{ transform: `scale(${pulse})`, textAlign: "center" }}>
          <div style={{
            fontFamily: "'Press Start 2P', monospace", fontSize: 120,
            color: "#ffffff",
            textShadow: `0 0 ${glow}px #00ffff, 0 0 ${glow * 2}px #00ffffaa, 0 0 ${glow * 3}px #00ffff50, 4px 4px 0 #002233`,
            letterSpacing: 10, lineHeight: 1,
          }}>TETRIS</div>
        </div>
        <div style={{ display: "flex", gap: 5 }}>
          {["#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600","#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff"].map((c, i) => (
            <div key={i} style={{ width: 24, height: 6, borderRadius: 2, backgroundColor: c, opacity: 0.9, boxShadow: `0 0 8px ${c}80` }} />
          ))}
        </div>
        <div style={{ transform: `scale(${pulse})`, textAlign: "center" }}>
          <div style={{
            fontFamily: "'Press Start 2P', monospace", fontSize: 86,
            color: "#00ff41",
            textShadow: `0 0 ${glow}px #00ff41, 0 0 ${glow * 2}px #00ff41aa, 0 0 ${glow * 3}px #00ff4150, 4px 4px 0 #003300`,
            letterSpacing: 8, lineHeight: 1,
          }}>VIBE CODING</div>
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.6) 100%)", pointerEvents: "none" }} />
      <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px)", pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
