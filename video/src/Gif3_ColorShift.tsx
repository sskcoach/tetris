import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";

// 배경 비 색상이 그린→시안→보라→그린 순환 + 타이틀 글로우 색도 변화
const TETRIMINO_ASCII = [
  "[][][][]", "[][]\n[][]", " []\n[][][]", "[]\n[][][]",
  "    []\n[][][]", " [][]\n[][]", "[][]\n [][]",
];

const generateRain = (count: number, seed0: number) => {
  const items: Array<{ x: number; speed: number; offset: number; piece: string; baseOpacity: number; size: number }> = [];
  for (let i = 0; i < count; i++) {
    const s = i * 6337 + seed0;
    items.push({
      x: (s * 13) % 1920,
      speed: 1.3 + ((s * 17) % 100) / 45,
      offset: ((s * 23) % 1400),
      piece: TETRIMINO_ASCII[(s * 11) % TETRIMINO_ASCII.length],
      baseOpacity: 0.18 + ((s * 29) % 100) / 350,
      size: 34 + ((s * 7) % 28),
    });
  }
  return items;
};

const rain = generateRain(100, 55);
const bright = generateRain(25, 99).map(r => ({ ...r, baseOpacity: r.baseOpacity * 2.3 }));

// HSL 색상 사이클
const hslColor = (hue: number, sat: number, light: number) =>
  `hsl(${hue}, ${sat}%, ${light}%)`;

export const Gif3_ColorShift: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const totalFrames = fps * 5;

  // 색상 사이클: 0→120(green) → 180(cyan) → 280(purple) → 120(green)
  const cycleProgress = (frame % totalFrames) / totalFrames;
  const hue = interpolate(cycleProgress, [0, 0.33, 0.66, 1], [120, 180, 280, 120]);
  const rainColor = hslColor(hue, 100, 55);
  const rainColorDim = hslColor(hue, 80, 40);
  const rainGlow = hslColor(hue, 100, 50);

  // 타이틀 글로우도 색상 변화
  const titleGlowColor = hslColor((hue + 60) % 360, 100, 70);

  // 펄스
  const pulse = interpolate(
    frame % (fps * 0.9),
    [0, fps * 0.12, fps * 0.24, fps * 0.45, fps * 0.55, fps * 0.9],
    [1, 1.04, 1, 1.04, 1, 1],
    { extrapolateRight: "clamp" }
  );

  const glow = interpolate(
    frame % (fps * 0.9),
    [0, fps * 0.12, fps * 0.24, fps * 0.45, fps * 0.55, fps * 0.9],
    [30, 50, 30, 42, 30, 30],
    { extrapolateRight: "clamp" }
  );

  // 배경 글로우 색상
  const bgGlow = hslColor(hue, 60, 15);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020808", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');`}</style>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 45%, ${bgGlow}80 0%, transparent 55%)` }} />

      {rain.map((r, i) => {
        const y = ((frame * r.speed + r.offset) % 1400) - 200;
        return (
          <pre key={`r${i}`} style={{
            position: "absolute", left: r.x, top: y,
            color: rainColorDim, opacity: r.baseOpacity,
            fontSize: r.size, fontFamily: "'Courier New', monospace",
            fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
            textShadow: `0 0 8px ${rainGlow}50`,
          }}>{r.piece}</pre>
        );
      })}
      {bright.map((r, i) => {
        const y = ((frame * r.speed + r.offset) % 1400) - 200;
        return (
          <pre key={`b${i}`} style={{
            position: "absolute", left: r.x, top: y,
            color: rainColor, opacity: Math.min(r.baseOpacity, 0.6),
            fontSize: r.size, fontFamily: "'Courier New', monospace",
            fontWeight: "bold", lineHeight: 1.1, whiteSpace: "pre", margin: 0,
            textShadow: `0 0 12px ${rainGlow}80, 0 0 24px ${rainGlow}40`,
          }}>{r.piece}</pre>
        );
      })}

      <AbsoluteFill style={{ background: "radial-gradient(ellipse 65% 50% at 50% 48%, rgba(0,0,0,0.6) 0%, transparent 100%)", pointerEvents: "none" }} />

      <AbsoluteFill style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 40 }}>
        <div style={{ transform: `scale(${pulse})`, textAlign: "center" }}>
          <div style={{
            fontFamily: "'Press Start 2P', monospace", fontSize: 180,
            color: "#ffffff",
            textShadow: `0 0 ${glow}px ${titleGlowColor}, 0 0 ${glow * 2}px ${titleGlowColor}aa, 0 0 ${glow * 3}px ${titleGlowColor}50, 6px 6px 0 #0a0a1a`,
            letterSpacing: 16, lineHeight: 1,
          }}>TETRIS</div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {["#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600","#00ffff","#ff3366","#ffff00","#00ff41","#cc00ff","#3366ff","#ff6600"].map((c, i) => (
            <div key={i} style={{ width: 34, height: 10, borderRadius: 2, backgroundColor: c, opacity: 0.9, boxShadow: `0 0 10px ${c}80` }} />
          ))}
        </div>
        <div style={{ transform: `scale(${pulse})`, textAlign: "center" }}>
          <div style={{
            fontFamily: "'Press Start 2P', monospace", fontSize: 130,
            color: rainColor,
            textShadow: `0 0 ${glow}px ${rainColor}, 0 0 ${glow * 2}px ${rainColor}aa, 0 0 ${glow * 3}px ${rainColor}50, 5px 5px 0 #0a0a0a`,
            letterSpacing: 12, lineHeight: 1,
          }}>VIBE CODING</div>
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.6) 100%)", pointerEvents: "none" }} />
      <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px)", pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
