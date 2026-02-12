// Shadow svg (light or dark) used to create glass effect

import { StyleSheet } from 'react-native';
import { Svg, Defs, LinearGradient, Stop, Rect } from 'react-native-svg';
import { Colors } from '@/theme';

export type ShadowProps = {
  light?: boolean;
  orientation?: "top" | "bottom" | "right" | "left";
  opacityStart?: string,
  opacityEnd?: string,
  borderRadius?: number,
  thickness?: number,
  color?: string
};

/**
 * Inner shadow used to simulate glass / depth.
 *
 * Renders an SVG gradient along one edge of the parent container.
 * Supports light (highlight) or dark (shadow) mode.
 *
 * @param light        If true → white highlight, else dark shadow
 * @param orientation  Edge where the shadow appears (top, bottom, left, right)
 * @param opacityStart Opacity at the edge (string for SVG, e.g. "0.2")
 * @param opacityEnd   Opacity fade value
 * @param borderRadius Corner rounding applied to the gradient rect
 * @param thickness    Size of the shadow strip in px
 */

export function Shadow({
  light = false,
  orientation = "top",
  opacityStart = "0.2",
  opacityEnd = "0",
  borderRadius = 0,
  thickness = 30,
  color=''
}: ShadowProps) {

  let x1 = "0%", y1 = "0%", x2 = "0%", y2 = "0%", x= "0%", y= "0%", width: string | number ="100%", height: string | number ="100%", transform = "";

  switch (orientation) {
    case "top":
      x1 = "0%"; y1 = "0%";
      x2 = "0%"; y2 = "100%";
      x = "0%"; y = "0%";
      transform = "translate(0, 0)";
      height = thickness;
      break;

    case "bottom":
      x1 = "0%"; y1 = "100%";
      x2 = "0%"; y2 = "0%";
      x = "0%"; y = "100%";
      transform = `translate(0, -${thickness})`;
      height = thickness;
      break;

    case "left":
      x1 = "0%"; y1 = "0%";
      x2 = "100%"; y2 = "0%";
      x = "0%"; y = "0%";
      transform = "translate(0, 0)";
      width = thickness;
      break;

    case "right":
      x1 = "100%"; y1 = "0%";
      x2 = "0%"; y2 = "0%";
      x = "100%"; y = "0%";
      transform = `translate(-${thickness}, 0)`;
      width = thickness;
      break;
  }

  const stopColor = color ? color : light ? Colors.light.lightShadow : Colors.light.darkShadow;

  console.log(stopColor)

  return (
    <Svg height="100%" width="100%" style={[StyleSheet.absoluteFill]}>
      <Defs>
        <LinearGradient id="grad" x1={x1} y1={y1} x2={x2} y2={y2}>
          <Stop offset="0%" stopColor={stopColor} stopOpacity={opacityStart} />
          <Stop offset="100%" stopColor={stopColor} stopOpacity={opacityEnd} />
        </LinearGradient>
      </Defs>
      <Rect
        x={x}
        y={y}
        width={width}
        height={height}
        fill="url(#grad)"
        rx={borderRadius}
        ry={borderRadius}
        transform={transform}
      />
    </Svg>
  )
}