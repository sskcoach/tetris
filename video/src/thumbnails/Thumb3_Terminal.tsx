import React from "react";
import { AbsoluteFill } from "remotion";

// 터미널 + 코드 라인 + 테트리스 결과물 좌우 배치
export const Thumb3_Terminal: React.FC = () => {
  const codeLines = [
    { prompt: true, text: "make tetris game" },
    { prompt: false, text: "✓ Creating game board..." },
    { prompt: false, text: "✓ Adding tetriminos..." },
    { prompt: false, text: "✓ Implementing controls..." },
    { prompt: false, text: "✓ Adding scoring system..." },
    { prompt: false, text: "✓ Game complete!" },
  ];

  // 간단한 테트리스 미니보드
  const MINI_CELL = 32;
  const MINI_COLS = 10;
  const miniBoard = [
    "..........","..........","..........","..........","..........","..........","..........","..........","..........","..........","...CC.....","..CCCT....","OOJJTT....",".OOJSTTZZ.","LLISSSZZII","LLITOOSSII","LLTTOOOSII","JJTTTSSIII",
  ];
  const colorMap: Record<string, string> = {
    I: "#00ffff", O: "#ffff00", T: "#cc00ff", S: "#00ff41",
    Z: "#ff3366", J: "#3366ff", L: "#ff6600", C: "#00ffcc",
  };

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d1117", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Fira+Code:wght@400;700&display=swap');`}</style>

      {/* 배경 */}
      <AbsoluteFill style={{
        background: "radial-gradient(ellipse at 30% 50%, rgba(0,50,80,0.3) 0%, transparent 60%), radial-gradient(ellipse at 80% 40%, rgba(0,80,50,0.2) 0%, transparent 50%)",
      }} />

      {/* 왼쪽: 터미널 */}
      <div style={{
        position: "absolute", left: 60, top: 100,
        width: 900, height: 880,
        background: "rgba(13, 17, 23, 0.95)",
        border: "1px solid #333",
        borderRadius: 16,
        overflow: "hidden",
        boxShadow: "0 20px 80px rgba(0,0,0,0.6)",
      }}>
        {/* 타이틀바 */}
        <div style={{
          height: 44, background: "#1c2130",
          display: "flex", alignItems: "center", padding: "0 16px", gap: 10,
        }}>
          <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#ff5f57" }} />
          <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#febc2e" }} />
          <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#28c840" }} />
          <span style={{ color: "#888", marginLeft: 16, fontFamily: "'Fira Code', monospace", fontSize: 16 }}>
            gemini-cli
          </span>
        </div>
        {/* 코드 */}
        <div style={{ padding: "24px 28px", fontFamily: "'Fira Code', monospace", fontSize: 26, lineHeight: 2.2 }}>
          {codeLines.map((line, i) => (
            <div key={i} style={{ display: "flex", gap: 8 }}>
              {line.prompt ? (
                <>
                  <span style={{ color: "#00ff41" }}>❯</span>
                  <span style={{ color: "#e0e0e0" }}>{line.text}</span>
                  <span style={{ display: "inline-block", width: 12, height: 26, backgroundColor: "#00ff41", opacity: 0.9 }} />
                </>
              ) : (
                <span style={{ color: "#58a6ff" }}>{line.text}</span>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 오른쪽: 게임 미니보드 */}
      <div style={{
        position: "absolute", right: 80, top: 100,
        border: "2px solid #333",
        borderRadius: 12,
        background: "rgba(0,0,0,0.6)",
        padding: 8,
        boxShadow: "0 10px 60px rgba(0,255,255,0.1)",
      }}>
        <div style={{ position: "relative", width: MINI_COLS * MINI_CELL, height: miniBoard.length * MINI_CELL }}>
          {miniBoard.map((row, r) =>
            row.split("").map((ch, c) => ch !== "." ? (
              <div key={`${r}-${c}`} style={{
                position: "absolute",
                left: c * MINI_CELL, top: r * MINI_CELL,
                width: MINI_CELL - 2, height: MINI_CELL - 2,
                backgroundColor: colorMap[ch] || "#666",
                border: `1px solid ${(colorMap[ch] || "#666")}88`,
                borderRadius: 2,
                boxShadow: `0 0 6px ${(colorMap[ch] || "#666")}40`,
              }} />
            ) : null)
          )}
        </div>
      </div>

      {/* 하단 타이틀 */}
      <div style={{
        position: "absolute", bottom: 40, width: "100%",
        textAlign: "center",
      }}>
        <span style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 80,
          color: "#00ffff",
          textShadow: "0 0 25px #00ffff, 0 0 50px #00ffff60, 3px 3px 0 #001122",
          letterSpacing: 6,
        }}>
          TETRIS
        </span>
        <span style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 40,
          color: "#ff6600",
          textShadow: "0 0 15px #ff6600, 2px 2px 0 #220800",
          marginLeft: 30,
          verticalAlign: "middle",
        }}>
          Original
        </span>
        <span style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 36,
          color: "#00ff41",
          textShadow: "0 0 15px #00ff41, 2px 2px 0 #002200",
          marginLeft: 40,
          verticalAlign: "middle",
        }}>
          VIBE CODING
        </span>
      </div>

      {/* 스캔라인 */}
      <AbsoluteFill style={{
        background: "repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.04) 3px, rgba(0,0,0,0.04) 6px)",
        pointerEvents: "none",
      }} />
    </AbsoluteFill>
  );
};
