import { Composition, Still } from "remotion";
import { HelloWorld, myCompSchema } from "./HelloWorld";
import { Logo, myCompSchema2 } from "./HelloWorld/Logo";
import { TetrisThumbnail } from "./TetrisThumbnail";
import { SampleA_LineClear } from "./SampleA_LineClear";
import { SampleB_AITyping } from "./SampleB_AITyping";
import { SampleC_RetroGlow } from "./SampleC_RetroGlow";
import { Gif1_RainPulse } from "./Gif1_RainPulse";
import { Gif2_GlitchFlicker } from "./Gif2_GlitchFlicker";
import { Gif3_ColorShift } from "./Gif3_ColorShift";
import { Gif4_AsciiPlay } from "./Gif4_AsciiPlay";
import {
  Thumb1_NeonBoard,
  Thumb2_BlockExplosion,
  Thumb3_Terminal,
  Thumb4_RetroArcade,
  Thumb5_MinimalBold,
  Thumb6_MatrixRain,
  Thumb7_MatrixCyan,
  Thumb8_MatrixPurple,
  Thumb9_MatrixGemini,
  Thumb10_MatrixDense,
  ThumbFinal,
  Thumb6v2,
  Thumb11_BrightPlay,
  Thumb12_AsciiPlay,
} from "./thumbnails";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        schema={myCompSchema}
        defaultProps={{
          titleText: "Welcome to Remotion",
          titleColor: "#000000",
          logoColor1: "#91EAE4",
          logoColor2: "#86A8E7",
        }}
      />
      <Composition
        id="OnlyLogo"
        component={Logo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        schema={myCompSchema2}
        defaultProps={{
          logoColor1: "#91dAE2" as const,
          logoColor2: "#86A8E7" as const,
        }}
      />
      <Composition
        id="TetrisThumbnail"
        component={TetrisThumbnail}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* === 썸네일 이미지 5종 === */}
      <Still id="thumb1-neon-board" component={Thumb1_NeonBoard} width={1920} height={1080} />
      <Still id="thumb2-block-explosion" component={Thumb2_BlockExplosion} width={1920} height={1080} />
      <Still id="thumb3-terminal" component={Thumb3_Terminal} width={1920} height={1080} />
      <Still id="thumb4-retro-arcade" component={Thumb4_RetroArcade} width={1920} height={1080} />
      <Still id="thumb5-minimal-bold" component={Thumb5_MinimalBold} width={1920} height={1080} />
      <Still id="thumb6-matrix-rain" component={Thumb6_MatrixRain} width={1920} height={1080} />
      <Still id="thumb7-matrix-cyan" component={Thumb7_MatrixCyan} width={1920} height={1080} />
      <Still id="thumb8-matrix-purple" component={Thumb8_MatrixPurple} width={1920} height={1080} />
      <Still id="thumb9-matrix-gemini" component={Thumb9_MatrixGemini} width={1920} height={1080} />
      <Still id="thumb10-matrix-dense" component={Thumb10_MatrixDense} width={1920} height={1080} />
      <Still id="thumb-final" component={ThumbFinal} width={1920} height={1080} />
      <Still id="thumb6v2" component={Thumb6v2} width={1920} height={1080} />
      <Still id="thumb11-bright-play" component={Thumb11_BrightPlay} width={1920} height={1080} />
      <Still id="thumb11-inflearn" component={Thumb11_BrightPlay} width={1200} height={781} />
      <Still id="thumb12-ascii-play" component={Thumb12_AsciiPlay} width={1920} height={1080} />
      <Still id="thumb12-inflearn" component={Thumb12_AsciiPlay} width={1200} height={781} />
      <Still id="inflearn-thumb" component={Gif1_RainPulse} width={1200} height={781} />

      {/* === 썸네일 샘플 3종 === */}
      <Composition
        id="sample-a-lineclear"
        component={SampleA_LineClear}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="sample-b-typing"
        component={SampleB_AITyping}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="sample-c-retroglow"
        component={SampleC_RetroGlow}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      {/* === GIF 프리뷰 (작은 사이즈) === */}
      <Composition
        id="gif-a"
        component={SampleA_LineClear}
        durationInFrames={75}
        fps={15}
        width={640}
        height={360}
      />
      <Composition
        id="gif-b"
        component={SampleB_AITyping}
        durationInFrames={75}
        fps={15}
        width={640}
        height={360}
      />
      <Composition
        id="gif-c"
        component={SampleC_RetroGlow}
        durationInFrames={75}
        fps={15}
        width={640}
        height={360}
      />
      {/* === 움짤 GIF v2 — 인프런 3:2 비율 (1080x720) === */}
      <Composition id="gif1-rain-pulse" component={Gif1_RainPulse} durationInFrames={75} fps={15} width={1080} height={720} />
      <Composition id="gif2-glitch" component={Gif2_GlitchFlicker} durationInFrames={75} fps={15} width={1080} height={720} />
      <Composition id="gif3-color-shift" component={Gif3_ColorShift} durationInFrames={75} fps={15} width={1080} height={720} />
      <Composition id="gif4-ascii-play" component={Gif4_AsciiPlay} durationInFrames={30} fps={3} width={1200} height={781} />
    </>
  );
};
