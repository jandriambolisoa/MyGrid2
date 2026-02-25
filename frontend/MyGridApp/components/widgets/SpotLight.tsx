import { Svg, Defs, RadialGradient, Stop, Rect } from 'react-native-svg';
import { StyleSheet } from 'react-native';

export type SpotLightProps = {
  color?: string,
  cx?: string,
  cy?: string,
  radius?: string,
  fx?: string,
  fy?: string,
  opacityStart?: string,
  opacityEnd?: string,
  borderRadius?: number
};

export function SpotLight({
  color = "#000000",
  cx = "50%",
  cy = "50%",
  radius = "50%",
  fx = "50%",
  fy = "50%",
  opacityStart = "0.8",
  opacityEnd = "0",
  borderRadius = 3
}: SpotLightProps) {
  return (
    <Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
      <Defs>
        <RadialGradient
          id="grad1"
          cx={cx}
          cy={cy}
          r={radius}
          fx={fx}
          fy={fy}
        >
          <Stop offset="0%" stopColor={color} stopOpacity={opacityStart} />
          <Stop offset="100%" stopColor={color} stopOpacity={opacityEnd} />
        </RadialGradient>
      </Defs>
      <Rect
        x="0"
        y="0"
        width="100%"
        height="100%"
        fill="url(#grad1)"
        rx={borderRadius}
        ry={borderRadius}
      />
    </Svg>
  )
}