import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";

// 글리치 + 플리커 — 타이틀이 랜덤하게 떨리고 색 번짐
const TETRIMINO_ASCII = [
  "[][][][]", "[][]\n[][]", " []\n[][][]", "[]\n[][][]",
  "    []\n[][][]", " [][]\n[][]", "[][]\n [][]",
];

const colors = ["#00ff41", "#00cc33", "#00ff66", "#33ff77", "#00dd44", "#00ffcc"];

const generateRain = (count: number, seed0: number) => {
  const items: Array<{ x: number; speed: number; offset: number; piece: string; opacity: number; size: number; color: string }> = [];
  for (let i = 0; i < count; i++) {
    const s = i * 5431 + seed0;
    items.push({
      x: (s * 13) % 1920,
      speed: 1.2 + ((s * 17) % 100) / 50,
      offset: ((s * 23) % 1400),
      piece: TETRIMINO_ASCII[(s * 11) % TETRIMINO_ASCII.length],
      opacity: 0.18 + ((s * 29) % 100) / 350,
      size: 34 + ((s * 7) % 28),
      color: colors[(s * 3) % colors.length],
    });
  }
  return items;
};

const rain = generateRain(100, 42);
const bright = generateRain(20, 88).map(r => ({ ...r, opacity: r.opacity * 2.5 }));

export const Gif2_GlitchFlicker: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 글리치: 특정 프레임에서 수평 오프셋
  const glitchSeed = Math.sin(frame * 127.1) * 10000;
  const isGlitch = (glitchSeed - Math.floor(glitchSeed)) > 0.92;
  const glitchX = isGlitch ? (Math.sin(frame * 73) * 15) : 0;
  const glitchY = isGlitch ? (Math.cos(frame * 91) * 5) : 0;

  // RGB 분리 (chromatic aberration)
  const rgbShift = isGlitch ? 6 : 0;

  // 밝기 플리커
  const flicker = isGlitch
    ? interpolate(Math.sin(frame * 200), [-1, 1], [0.7, 1])
    : 1;

  // 기본 펄스
  const pulse = interpolate(
    frame % (fps * 1),
    [0, fps * 0.15, fps * 0.3, fps * 0.55, fps * 0.65, fps * 1],
    [1, 1.04, 1, 1.04, 1, 1],
    { extrapolateRight: "clamp" }
  );

  const glow = interpolate(
    frame % (fps * 1),
    [0, fps * 0.15, fps * 0.3, fps * 0.55, fps * 0.65, fps * 1],
    [30, 50, 30, 42, 30, 30],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#020a02", overflow: "hidden", opacity: flicker }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, rgba(0,60,0,0.5) 0%, transparent 55%)" }} />

      {rain.map((r, i) => {
        const y = ((frame * r.speed + r.offset) % 1400) - 200;
        return (
          <pre key={`r${i}`} style={{
            position: "absolute", left: r.x, top: y,
            color: r.color, opacity: r.opacity,
            fontSize: r.size, fontFamily: "'Courier New', monospace",
            fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
            textShadow: `0 0 8px ${r.color}50`,
          }}>{r.piece}</pre>
        );
      })}
      {bright.map((r, i) => {
        const y = ((frame * r.speed + r.offset) % 1400) - 200;
        return (
          <pre key={`b${i}`} style={{
            position: "absolute", left: r.x, top: y,
            color: r.color, opacity: Math.min(r.opacity, 0.6),
            fontSize: r.size, fontFamily: "'Courier New', monospace",
            fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
            textShadow: `0 0 12px ${r.color}80`,
          }}>{r.piece}</pre>
        );
      })}

      <AbsoluteFill style={{ background: "radial-gradient(ellipse 65% 50% at 50% 48%, rgba(0,0,0,0.6) 0%, transparent 100%)", pointerEvents: "none" }} />

      {/* 글리치 수평 라인 */}
      {isGlitch && (
        <div style={{
          position: "absolute",
          left: 0, top: 200 + (frame * 37) % 600,
          width: "100%", height: 4,
          backgroundColor: "rgba(0,255,65,0.3)",
        }} />
      )}

      <AbsoluteFill style={{
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 40,
        transform: `translate(${glitchX}px, ${glitchY}px)`,
      }}>
        <div style={{ transform: `scale(${pulse})`, textAlign: "center", position: "relative" }}>
          {/* RGB 분리 레이어 */}
          {rgbShift > 0 && (
            <>
              <div style={{
                position: "absolute", left: -rgbShift, top: 0,
                fontFamily: "'Press Start 2P', monospace", fontSize: 180,
                color: "rgba(255,0,0,0.4)", letterSpacing: 16, lineHeight: 1,
                mixBlendMode: "screen",
              }}>TETRIS</div>
              <div style={{
                position: "absolute", left: rgbShift, top: 0,
                fontFamily: "'Press Start 2P', monospace", fontSize: 180,
                color: "rgba(0,100,255,0.4)", letterSpacing: 16, lineHeight: 1,
                mixBlendMode: "screen",
              }}>TETRIS</div>
            </>
          )}
          <div style={{
            fontFamily: "'Press Start 2P', monospace", fontSize: 180,
            color: "#ffffff",
            textShadow: `0 0 ${glow}px #00ffff, 0 0 ${glow * 2}px #00ffffaa, 0 0 ${glow * 3}px #00ffff50, 6px 6px 0 #002233`,
            letterSpacing: 16, lineHeight: 1,
          }}>TETRIS</div>
        </div>

        <div style={{ display: "flex", gap: 8 }}>
          {["#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600","#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600"].map((c, i) => (
            <div key={i} style={{ width: 34, height: 10, borderRadius: 2, backgroundColor: c, opacity: 0.9, boxShadow: `0 0 10px ${c}80` }} />
          ))}
        </div>

        <div style={{ transform: `scale(${pulse})`, textAlign: "center", position: "relative" }}>
          {rgbShift > 0 && (
            <>
              <div style={{
                position: "absolute", left: -rgbShift, top: 0,
                fontFamily: "'Press Start 2P', monospace", fontSize: 130,
                color: "rgba(255,0,0,0.4)", letterSpacing: 12, lineHeight: 1,
                mixBlendMode: "screen",
              }}>VIBE CODING</div>
              <div style={{
                position: "absolute", left: rgbShift, top: 0,
                fontFamily: "'Press Start 2P', monospace", fontSize: 130,
                color: "rgba(0,100,255,0.4)", letterSpacing: 12, lineHeight: 1,
                mixBlendMode: "screen",
              }}>VIBE CODING</div>
            </>
          )}
          <div style={{
            fontFamily: "'Press Start 2P', monospace", fontSize: 130,
            color: "#00ff41",
            textShadow: `0 0 ${glow}px #00ff41, 0 0 ${glow * 2}px #00ff41aa, 0 0 ${glow * 3}px #00ff4150, 5px 5px 0 #003300`,
            letterSpacing: 12, lineHeight: 1,
          }}>VIBE CODING</div>
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.6) 100%)", pointerEvents: "none" }} />
      <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px)", pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
